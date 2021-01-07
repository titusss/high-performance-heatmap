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
      :layerSettings="layerSettings"
      :colorGradientDict="colorGradientDict"
      :minMaxValues="[this.lowestValue, this.highestValue]"
    />
    <cameraMenu
      class="camera_menu menu_c"
      :activeCamera="activeCamera"
      :elevationScale="layerSettings.gridCellLayer.elevationScale"
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
      updateTriggerObjects: {
        gradientUpdateTrigger: false,
        elevationScale: 200,
      },
      colorGradientPreset: null,
      highestValue: null,
      lowestValue: null,
      colorGradientDict: {},
      colorGradient: null,
      advancedLighting: false,
      subTables: {},
      layerSettings: {
        gridCellLayer: {
          id: 'grid-gridCellLayerCell-layer',
          data: null,
          getPosition: (d) => d.COORDINATES,
          getElevation: (d) => d.VALUE,
          getFillColor: (d) => this.colorGradientDict[d.TITLE](d.VALUE).rgb(),
        },
        textCellLayer: {
          id: 'text-cell-layer',
          data: null,
          sizeUnits: 'meters',
          getPosition: (d) => d.COORDINATES,
          getText: (d) => d.VALUE,
          // PERFORMANCE: Scale text based on the strings length
          getSize: (d) => 1575 / (String(d.VALUE).length + 2.5),
          getAngle: 90,
          getTextAnchor: 'middle',
          getAlignmentBaseline: 'center',
          billboard: false,
          fontFamily:
            '-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif',
          fontWeight: 'bold',
        },
        rowTextLayer: {
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
        columnTextLayer: {
          id: 'column-text-layer',
          data: null,
          sizeUnits: 'meters',
          getPosition: (d) => d.COORDINATES,
          getText: (d) => d.VALUE,
          getSize: 450,
          getAngle: 180,
          getTextAnchor: 'start',
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
        minZoom: 4,
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
      // Disable Retina rendering for better performance:
      // useDevicePixels: false,
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
        gradient: {},
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
      // new rowTextLayer(this.layerSettings.rowTextLayer)] })
      this.settings.layer = {
        ...this.settings.layer,
        ...e.layerSettings.gridCellLayer,
      };
    },
    updateSettings(updatedSettings) {
      const s = updatedSettings.settings;
      // It might be useful to use a switch case instead,
      // if the possible conditions grow beyond 5 items.
      switch (updatedSettings.type) {
        case 'layer':
          this.layerSettings.gridCellLayer = {
            ...this.layerSettings.gridCellLayer,
            ...s,
          };
          this.layerSettings.gridCellLayer.elevationScale = Number(
            s.elevationScale,
          ); // This is necessary because bootstrap converts the property to a string.
          this.updateTriggerObjects.elevationScale = this
            .layerSettings.gridCellLayer.elevationScale;
          if (s.advancedMaterial) {
            this.layerSettings.gridCellLayer.material = {
              ambient: Number(s.ambientMaterial),
              diffuse: Number(s.diffuseMaterial),
              shininess: Number(s.shininess),
            };
          }
          if (this.lowestValue < 0) {
            this.layerSettings.gridCellLayer.updateTriggers = {
              getFillColor: [
                this.updateTriggerObjects.gradientUpdateTrigger,
              ],
              getPosition: this.updateTriggerObjects.elevationScale,
            };
          } else {
            this.layerSettings.gridCellLayer.updateTriggers = {
              getFillColor: [
                this.updateTriggerObjects.gradientUpdateTrigger,
              ],
            };
          }
          this.deck.setProps({
            layers: [
              new GridCellLayer(this.layerSettings.gridCellLayer),
              new TextLayer(this.layerSettings.textCellLayer),
              new TextLayer(this.layerSettings.rowTextLayer),
              new TextLayer(this.layerSettings.columnTextLayer),
            ],
          });
          break;
        case 'gradient':
          this.updateTriggerObjects.gradientUpdateTrigger = !this
            .updateTriggerObjects.gradientUpdateTrigger;
          this.colorGradientPreset = s.gradientPreset.value;
          if (this.colorGradientPreset !== s.gradientPreset.value
          || s.individualGradients === false) {
            Object.keys(this.subTables).forEach((subTableTitle) => {
              this.colorGradientDict[subTableTitle] = chroma
                .scale(this.colorGradientPreset)
                .domain(s.gradientPreset.domain);
            });
          } else {
            Object.keys(this.subTables).forEach((subTableTitle) => {
              this.colorGradientDict[subTableTitle] = chroma
                .scale(s[subTableTitle].value)
                .domain(s[subTableTitle].domain);
            });
          }
          if (this.lowestValue < 0) {
            this.layerSettings.gridCellLayer.updateTriggers = {
              getFillColor: [
                this.updateTriggerObjects.gradientUpdateTrigger,
              ],
              getPosition: this.updateTriggerObjects.elevationScale,
            };
          } else {
            this.layerSettings.gridCellLayer.updateTriggers = {
              getFillColor: [
                this.updateTriggerObjects.gradientUpdateTrigger,
              ],
            };
          }
          this.deck.setProps({
            layers: [
              new GridCellLayer(this.layerSettings.gridCellLayer),
              new TextLayer(this.layerSettings.textCellLayer),
              new TextLayer(this.layerSettings.rowTextLayer),
              new TextLayer(this.layerSettings.columnTextLayer),
            ],
          });
          break;
        case 'lighting':
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
          break;
        default:
          console.log('Warning: No case found for this setting update.');
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
            this.layerSettings.textCellLayer.data,
            this.layerSettings.rowTextLayer.data,
            this.layerSettings.columnTextLayer.data,
            this.highestValue,
            this.lowestValue,
          ] = this.processJsonData(res.data);
          this.createSubTableGradientForms();
          if (this.lowestValue < 0) {
            this.configureNegativeValues();
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    processJsonData(json) {
      // This could be moved to the python backend for performace reasons.
      const gridCellLayerData = [];
      const textCellLayerData = [];
      const rowTextLayerData = [];
      const columnTextLayerData = [];
      const columns = Object.keys(json[0]);
      let lowestValue = 0;
      let highestValue = 0;
      let subTableLowestValue = 0;
      let subTableHighestValue = 0;
      let lastPrefix;
      let columnName;
      let columnCoordinate = -1;
      let scaledColumnCoordinate = 0;
      for (let columnIndex = 0; columnIndex < columns.length; columnIndex += 1) {
        if (columnIndex !== 0) {
          if (columns[columnIndex].startsWith('(') && columns[columnIndex].includes(') ')) {
            const splitIndex = columns[columnIndex].indexOf(') ');
            const prefix = columns[columnIndex].slice(0, splitIndex + 1);
            if (prefix !== lastPrefix) {
              lastPrefix = prefix;
              subTableLowestValue = 0;
              subTableHighestValue = 0;
              columnCoordinate += 1.4;
              columnName = columns[columnIndex].slice(splitIndex + 2);
            } else {
              columnCoordinate += 1;
            }
          } else {
            columnName = columns[columnIndex];
            columnCoordinate += 1;
          }
          // Only calculate x coordinate when the column changes.
          scaledColumnCoordinate = columnCoordinate / 140;
          columnTextLayerData.push({
            COORDINATES: [
              -this.constants.textMarginTop,
              scaledColumnCoordinate - this.constants.textMarginRight,
            ],
            VALUE: Object.keys(json[0])[columnIndex],
          });
        }
        for (let rowIndex = 0; rowIndex < json.length; rowIndex += 1) {
          if (columnIndex !== 0) {
            if (Number.isFinite(json[rowIndex][columns[columnIndex]])) {
              const gridCellLayerCell = {
                COLUMN: columnName,
                COORDINATES: [rowIndex / 140, scaledColumnCoordinate],
                ROW: json[rowIndex][columns[0]],
                VALUE: json[rowIndex][columns[columnIndex]],
                TITLE: lastPrefix,
              };
              if (gridCellLayerCell.VALUE > subTableHighestValue) {
                subTableHighestValue = gridCellLayerCell.VALUE;
                if (gridCellLayerCell.VALUE > highestValue) {
                  highestValue = gridCellLayerCell.VALUE;
                }
              }
              if (gridCellLayerCell.VALUE < subTableLowestValue) {
                subTableLowestValue = gridCellLayerCell.VALUE;
                if (gridCellLayerCell.VALUE < lowestValue) {
                  lowestValue = gridCellLayerCell.VALUE;
                }
              }
              if (gridCellLayerCell.VALUE < 0) {
                gridCellLayerCell.VALUE *= -1;
                gridCellLayerCell.ORIENTATION = -1;
              }
              gridCellLayerData.push(gridCellLayerCell);
            } else {
              const textCellLayerCell = {
                COLUMN: columnName,
                COORDINATES: [
                  rowIndex / 140 + this.constants.textMarginTop,
                  scaledColumnCoordinate + this.constants.textMarginTop,
                ],
                ROW: json[rowIndex][columns[0]],
                VALUE: json[rowIndex][columns[columnIndex]],
              };
              textCellLayerData.push(textCellLayerCell);
            }
          } else {
            rowTextLayerData.push({
              COORDINATES: [
                rowIndex / 140 + this.constants.textMarginTop,
                scaledColumnCoordinate,
              ],
              VALUE: json[rowIndex][columns[columnIndex]],
            });
          }
        }
        if (lastPrefix) {
          this.subTables[lastPrefix] = {
            TITLE: lastPrefix,
            LOWEST_VALUE: subTableLowestValue,
            HIGHEST_VALUE: subTableHighestValue,
          };
        }
      }
      return [
        gridCellLayerData,
        textCellLayerData,
        rowTextLayerData,
        columnTextLayerData,
        highestValue,
        lowestValue,
      ];
    },
    configureNegativeValues() {
      this.layerSettings.gridCellLayer.getPosition = (d) => [d.COORDINATES[0],
        d.COORDINATES[1], d.VALUE * (this.updateTriggerObjects.elevationScale * d.ORIENTATION)];
      this.layerSettings.gridCellLayer.getFillColor = (d) => ((!d.ORIENTATION)
        ? this.colorGradientDict[d.TITLE](d.VALUE).rgb()
        : this.colorGradientDict[d.TITLE](d.VALUE * d.ORIENTATION).rgb());
    },
    createSubTableGradientForms() {
      for (let i = 0; i < this.settingsTemplate.basicSettings.settings.length; i += 1) {
        if (this.settingsTemplate.basicSettings.settings[i].label === 'Color Gradient') {
          for (
            let j = 0; j < this.settingsTemplate.basicSettings.settings[i].inputs.length; j += 1
          ) {
            if (this.settingsTemplate.basicSettings.settings[i].inputs[j].id === 'gradientPreset') {
              Object.keys(this.subTables).forEach((subTableTitle) => {
                // We need to DEEP clone this template object.
                // The only way to remove reactivity seems to parse it as an JSON object.
                // This is questionable but right now the least bad way to clone it.
                let gradientFormTemplate = JSON.parse(JSON.stringify(
                  this.settingsTemplate.basicSettings.settings[i].inputs[j],
                ));
                gradientFormTemplate.label = subTableTitle;
                gradientFormTemplate.id = gradientFormTemplate.label;
                gradientFormTemplate.condition = true;
                gradientFormTemplate = this.calculateGradientDomain(
                  gradientFormTemplate,
                  this.subTables[subTableTitle].LOWEST_VALUE,
                  this.subTables[subTableTitle].HIGHEST_VALUE,
                );
                this.settings.gradient[gradientFormTemplate.id] = gradientFormTemplate.value;
                this.settingsTemplate.basicSettings.settings[i].inputs.push(gradientFormTemplate);
              });
              this.settingsTemplate.basicSettings.settings[i].inputs[j] = this
                .calculateGradientDomain(
                  settingsTemplate.basicSettings.settings[i].inputs[j],
                  this.lowestValue,
                  this.highestValue,
                );
              break;
            }
          }
          break;
        }
      }
    },
    calculateGradientDomain(form, lowestValue, highestValue) {
      // Calculate order of magnitude of the value range between data min and max.
      const gradientFormTemplate = form;
      gradientFormTemplate.min = lowestValue;
      gradientFormTemplate.max = highestValue;
      gradientFormTemplate.orderOfMagnitude = Math
        .floor(Math.log10(Math.abs(highestValue - lowestValue)));
      gradientFormTemplate.interval = 10 ** (gradientFormTemplate.orderOfMagnitude - 3);
      // The following uses EPSILON to round to n decimal places, where n is
      // determined by the Order of Magnitude of the range between min and max
      // This means that the mid points of data with ranges such as 0.0001 will be
      // differently rounded than ranges like 10000. This isn't completely crucial,
      // but improves UX by determining the gradient slider interval and the overall
      // length and precision of the mid point number.
      gradientFormTemplate.mid = Math.round(
        ((highestValue
          - lowestValue) / 2
          + lowestValue) * 10 ** (-gradientFormTemplate.orderOfMagnitude + 3)
          + Number.EPSILON,
      ) / 10 ** (-gradientFormTemplate.orderOfMagnitude + 3);
      gradientFormTemplate.value.domain = [
        lowestValue,
        gradientFormTemplate.mid,
        highestValue,
      ];
      return gradientFormTemplate;
    },
    getTooltip({ object }) {
      if (!object) {
        return null;
      }
      const column = object.COLUMN;
      const row = object.ROW;
      let count;
      if (!object.ORIENTATION) {
        count = object.VALUE;
      } else {
        count = object.VALUE * object.ORIENTATION;
      }
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
