<!-- App / deckglCanvas -->
<template>
  <div>
    <div id="export_svg"></div>
    <mainMenu
      v-if="layerSettings.gridCellLayer.data"
      class="main_menu menu_c"
      @settings-changed="updateSettings"
      @take-screenshot="takeScreenshot"
      @active-camera-selected="changeCamera"
      :settings="settings"
      :settingsTemplate="settingsTemplate"
      :layerSettings="layerSettings.gridCellLayer"
      :colorGradient="colorGradient"
    />
    <cameraMenu
      class="camera_menu menu_c"
      :activeCamera="activeCamera"
      @active-camera-selected="changeCamera"
    />
    <div class="deck-container" id="deck-container">
      <canvas id="deck-canvas" ref="canvas"></canvas>
    </div>
  </div>
</template>

<script>
import {
  Deck,
  LightingEffect,
  AmbientLight,
  DirectionalLight,
} from '@deck.gl/core';
import { GridCellLayer, TextLayer } from '@deck.gl/layers';
import axios from 'axios';
import chroma from 'chroma-js';
import cameraMenu from './cameraMenu.vue';
import mainMenu from './mainMenu.vue';
import settingsTemplate from '../assets/settingsTemplate.json';

export default {
  components: {
    cameraMenu,
    mainMenu,
  },
  data() {
    return {
      // backendUrl: 'http://127.0.0.1:5000',
      // backendUrl: 'https://hp-heatmap-backend-44nub6ij6q-ez.a.run.app',
      backendUrl: 'http://hiri-heatmap-backend.test.fedcloud.eu',
      activeCamera: '3D',
      constants: {
        textMarginRight: -0.003,
        textMarginTop: 0.5 / 140,
      },
      highestValue: null,
      lowestValue: null,
      colorGradient: null,
      colorGradientPreset: null,
      advancedLighting: false,
      layerSettings: {
        gridCellLayer: {
          id: 'grid-gridCellLayerCell-layer',
          data: null,
          getPosition: (d) => d.COORDINATES,
          getElevation: (d) => d.VALUE,
          getFillColor: (d) => this.colorGradient(d.VALUE).rgb(),
          updateTriggers: { getFillColor: this.colorGradientPreset },
        },
        textLayer: {
          id: 'row-text-layer',
          data: null,
          sizeUnits: 'meters',
          getPosition: (d) => d.COORDINATES,
          getText: (d) => d.VALUE,
          getSize: 450,
          getAngle: 90,
          getTextAnchor: 'end',
          getAlignmentBaseline: 'center',
          billboard: false,
          fontFamily:
            '-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif',
        },
      },
      currentViewState: {
        latitude: 0.02,
        longitude: 0.05,
        zoom: 11,
        minZoom: 2,
        pitch: 40,
        maxPitch: 89,
        bearing: -40,
      },
      settingsTemplate,
      settings: null,
    };
  },
  created() {
    this.fetchData(`${this.backendUrl}/config`);
    this.deck = null;
    this.settings = this.generateSettings();
  },
  mounted() {
    this.deck = new Deck({
      canvas: this.$refs.canvas,
      viewState: this.currentViewState,
      getTooltip: this.getTooltip,
      onViewStateChange: ({ viewState }) => {
        this.currentViewState = viewState;
        this.deck.setProps({ viewState: this.currentViewState });
      },
      controller: true,
    });
    // this.deck.layerManager.layers[0].props.elevationScale = 10
  },
  methods: {
    takeScreenshot() {
      this.deck.redraw(true);
      const { canvas } = this.deck;
      document.getElementById('deck-container').appendChild(canvas);
      const a = document.createElement('a');
      // toDataURL defaults to png, so we need to request a jpeg, then convert for file download.
      a.href = canvas.toDataURL('image/png').replace('image/png', 'image/octet-stream');
      a.download = 'screenshot.png';
      a.click();
    },
    generateSettings() {
      const settings = {
        layer: {},
        lighting: {},
        custom: {},
      };
      Object.keys(settingsTemplate).forEach((mode) => {
        for (let i = 0; i < settingsTemplate[mode].settings.length; i += 1) {
          for (
            let j = 0;
            j < settingsTemplate[mode].settings[i].inputs.length;
            j += 1
          ) {
            const input = settingsTemplate[mode].settings[i].inputs[j];
            settings[input.propertyType][input.id] = input.value;
          }
        }
      });
      return settings;
    },
    changeCamera(e) {
      this.activeCamera = e.id;
      this.currentViewState = { ...this.currentViewState, ...e.viewState };
      this.deck.setProps({ viewState: this.currentViewState });
      this.layerSettings.gridCellLayer = {
        ...this.layerSettings.gridCellLayer,
        ...e.layerSettings.gridCellLayer,
      };
      // this.deck.setProps({ layers: [new GridCellLayer(this.layerSettings.gridCellLayer),
      // new TextLayer(this.layerSettings.textLayer)] })
      this.settings.layer = {
        ...this.settings.layer,
        ...e.layerSettings.gridCellLayer,
      };
    },
    updateSettings(updatedSettings) {
      const s = updatedSettings.settings;
      // It might be useful to use a switch case instead,
      // if the possible conditions grow beyond 5 items.
      if (updatedSettings.type === 'layer') {
        this.layerSettings.gridCellLayer = {
          ...this.layerSettings.gridCellLayer,
          ...s,
        };
        if (this.colorGradientPreset !== s.gradientPreset.value) {
          this.colorGradientPreset = s.gradientPreset.value;
          this.colorGradient = chroma
            .scale(this.colorGradientPreset)
            .domain([this.lowestValue, this.highestValue]);
          this.layerSettings.gridCellLayer.updateTriggers = {
            getFillColor: this.colorGradientPreset,
          };
        }
        this.layerSettings.gridCellLayer.elevationScale = Number(
          s.elevationScale,
        ); // This is necessary because Vue.js converts the property to a string.
        if (s.advancedMaterial) {
          this.layerSettings.gridCellLayer.material = {
            ambient: Number(s.ambientMaterial),
            diffuse: Number(s.diffuseMaterial),
            shininess: Number(s.shininess),
          };
        }
        this.deck.setProps({
          layers: [
            new GridCellLayer(this.layerSettings.gridCellLayer),
            new TextLayer(this.layerSettings.textLayer),
          ],
        });
      } else if (updatedSettings.type === 'lighting') {
        if (s.advancedLighting === true) {
          // Only build new lights when advanced light is activated.
          // Probably not necessary but I speculate on performance advantages with this approach.
          const ambient = new AmbientLight({
            color: [255, 255, 255],
            intensity: s.ambientLight,
          });
          const directionalLight1 = new DirectionalLight({
            color: [255, 255, 255],
            direction: [this.highestValue / 2, 5, 3000],
            intensity: s.directionalLight1,
          });
          const directionalLight2 = new DirectionalLight({
            color: [255, 255, 255],
            position: [this.highestValue / 4, 0.1, 1000],
            intensity: s.directionalLight2,
          });
          this.deck.setProps({
            effects: [
              new LightingEffect({
                ambient,
                directionalLight1,
                directionalLight2,
              }),
            ],
          });
        } else {
          this.deck.setProps({ effects: [] });
        }
      }
      this.$emit('long-loading-finished');
    },
    fetchData(url) {
      const payload = new FormData();
      payload.append('url', JSON.stringify(this.$route.query.config));
      axios
        .post(url, payload)
        .then((res) => {
          [
            this.layerSettings.gridCellLayer.data,
            this.layerSettings.textLayer.data,
            this.highestValue,
            this.lowestValue,
          ] = this.processJsonData(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    processJsonData(json) {
      // This could be moved to the python backend for performace reasons.
      const gridCellLayerData = [];
      const textLayerData = [];
      const columns = Object.keys(json[0]);
      let lowestValue = 0;
      let highestValue = 0;
      let lastPrefix;
      let columnName;
      let columnCoordinate = 0;
      for (let columnIndex = 0; columnIndex < columns.length; columnIndex += 1) {
        if (columns[columnIndex].startsWith('(')) {
          const splitIndex = columns[columnIndex].indexOf(') ');
          const prefix = columns[columnIndex].slice(0, splitIndex + 1);
          if (prefix !== lastPrefix) {
            lastPrefix = prefix;
            columnCoordinate += 1.4;
          } else {
            columnCoordinate += 1;
          }
          columnName = columns[columnIndex].slice(splitIndex + 2);
        } else {
          columnName = columns[columnIndex];
        }
        // Only calculate x coordinate when the column changes.
        const scaledColumnCoordinate = columnCoordinate / 140;
        for (let rowIndex = 0; rowIndex < json.length; rowIndex += 1) {
          const gridCellLayerCell = {
            COLUMN: columnName,
            COORDINATES: [rowIndex / 140, scaledColumnCoordinate],
            ROW: json[rowIndex][columns[0]],
            VALUE: json[rowIndex][columns[columnIndex]],
          };
          gridCellLayerData.push(gridCellLayerCell);
          if (
            gridCellLayerCell.VALUE > highestValue
            && gridCellLayerCell.VALUE !== Infinity
            && gridCellLayerCell.VALUE !== -Infinity
          ) {
            highestValue = gridCellLayerCell.VALUE;
          }
          if (
            gridCellLayerCell.VALUE < lowestValue
            && gridCellLayerCell.VALUE !== -Infinity
            && gridCellLayerCell.VALUE !== Infinity
          ) {
            lowestValue = gridCellLayerCell.VALUE;
          }
          if (columnIndex === 0) {
            textLayerData.push({
              COORDINATES: [
                gridCellLayerCell.COORDINATES[0] + this.constants.textMarginTop,
                this.constants.textMarginRight,
              ],
              VALUE: gridCellLayerCell.ROW,
            });
          }
        }
      }
      return [gridCellLayerData, textLayerData, highestValue, lowestValue];
    },
    getTooltip({ object }) {
      if (!object) {
        return null;
      }
      const column = object.COLUMN;
      const row = object.ROW;
      const count = object.VALUE;
      return {
        html: `\
        ${column}<br>
        ${row}<br>
        <strong>${count}</strong>`,
        // Below is an example for custom CSS styling for the tooltip.
        // style: {
        //   backgroundColor: '#000',
        //   margin: '0'
        // }
      };
      // Below is an example for a more advanced tooltip format according to: https://github.com/visgl/deck.gl/blob/8.3-release/examples/website/3d-heatmap/app.js
      // const lat = object.COORDINATES[1]
      // const lng = object.COORDINATES[0]
      // return `\
      //   latitude: ${Number.isFinite(lat) ? lat.toFixed(6) : ''}
      //   longitude: ${Number.isFinite(lng) ? lng.toFixed(6) : ''}
      //   ${count} Accidents`
    },
  },
};
</script>

<style scoped>
.deck-container {
  width: 100vw;
  height: 100vh;
  position: relative;
}
#deckgl-overlay {
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
}

.camera_menu {
  top: 10px;
  right: 10px;
}

.main_menu {
  top: 10px;
  left: 10px;
}
.menu_c {
  position: absolute;
  z-index: 1000;
}
#export_svg {
  display: none;
}
</style>
