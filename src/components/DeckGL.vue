<template>
  <div>
    <cameraMenu class="camera_menu menu_c" :activeCamera="activeCamera" @active-camera-selected="changeCamera"/>
    <div class="deck-container">
      <canvas id="deck-canvas" ref="canvas"></canvas>
    </div>
    <settingsMenu
      v-if="layerSettings.gridCellLayer.data"
      class="settings_menu menu_c"
      @settingsChanged="updateSettings"
      :globalSettings="layerSettings.gridCellLayer"
    />
  </div>
</template>

<script>
import {
  Deck,
  LightingEffect,
  AmbientLight,
  DirectionalLight
} from '@deck.gl/core'
import { GridCellLayer, TextLayer } from '@deck.gl/layers'
import axios from 'axios'
import settingsMenu from '@/components/settingsMenu.vue'
import cameraMenu from '@/components/cameraMenu.vue'
import chroma from 'chroma-js'
export default {
  components: {
    settingsMenu,
    cameraMenu
  },
  data () {
    return {
      // backendUrl: 'http://127.0.0.1:5000',
      backendUrl: 'https://hp-heatmap-backend-44nub6ij6q-ez.a.run.app',
      activeCamera: '3D',
      constants: {
        textMarginRight: -0.003,
        textMarginTop: 0.5 / 140
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
          getPosition: d => d.COORDINATES,
          getElevation: d => d.VALUE,
          getFillColor: d => this.colorGradient(d.VALUE).rgb(),
          updateTriggers: { getFillColor: this.colorGradientPreset }
        },
        textLayer: {
          id: 'row-text-layer',
          data: null,
          sizeUnits: 'meters',
          getPosition: d => d.COORDINATES,
          getText: d => d.VALUE,
          getSize: 450,
          getAngle: 90,
          getTextAnchor: 'end',
          getAlignmentBaseline: 'center',
          billboard: false,
          fontFamily: '-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif'
        }
      },
      currentViewState: {
        latitude: 0.02,
        longitude: 0.05,
        zoom: 11,
        minZoom: 2,
        pitch: 40,
        bearing: -40
      },
      colorSchemes: {
        sequential: [
          'BuGn',
          'BuPu',
          'GnBu',
          'OrRd',
          'PuBu',
          'PuBuGn',
          'PuRd',
          'RdPu',
          'YlGn',
          'YlGnBu',
          'YlOrBr',
          'YlOrRd'
        ],
        singlehue: ['Blues', 'Greens', 'Greys', 'Oranges', 'Purples', 'Reds'],
        diverging: [
          'BrBG',
          'PiYG',
          'PRGn',
          'PuOr',
          'RdBu',
          'RdGy',
          'RdYlBu',
          'RdYlGn',
          'Spectral'
        ],
        qualitative: [
          'Accent',
          'Dark2',
          'Paired',
          'Pastel1',
          'Pastel2',
          'Set1',
          'Set2',
          'Set3'
        ]
      }
    }
  },
  created () {
    this.fetchData(`${this.backendUrl}/config`)
    this.deck = null
  },
  mounted () {
    this.deck = new Deck({
      canvas: this.$refs.canvas,
      viewState: this.currentViewState,
      getTooltip: this.getTooltip,
      onViewStateChange: ({ viewState }) => {
        this.currentViewState = viewState
        this.deck.setProps({ viewState: this.currentViewState })
      },
      controller: true
    })
    // this.deck.layerManager.layers[0].props.elevationScale = 10
  },
  methods: {
    changeCamera (e) {
      this.activeCamera = e.id
      this.currentViewState = Object.assign({}, this.currentViewState, e.viewState)
      this.layerSettings.gridCellLayer = Object.assign({}, this.layerSettings.gridCellLayer, e.layerSettings.gridCellLayer)
      this.deck.setProps({ viewState: this.currentViewState })
      this.deck.setProps({ layers: [new GridCellLayer(this.layerSettings.gridCellLayer), new TextLayer(this.layerSettings.textLayer)] })
    },
    updateSettings (updatedSettings) {
      const s = updatedSettings.settings
      // It might be useful to use a switch case instead, if the possible conditions grow beyond 5 items.
      if (updatedSettings.type === 'layer') {
        this.layerSettings.gridCellLayer = Object.assign(s, this.layerSettings.gridCellLayer)
        if (this.colorGradientPreset !== s.gradientPreset.value) {
          this.colorGradientPreset = s.gradientPreset.value
          this.colorGradient = chroma
            .scale(this.colorGradientPreset)
            .domain([this.lowestValue, this.highestValue])
          this.layerSettings.gridCellLayer.updateTriggers = { getFillColor: this.colorGradientPreset }
        }
        this.layerSettings.gridCellLayer.elevationScale = Number(s.elevationScale) // This is necessary because Vue.js converts the property to a string.
        this.deck.setProps({ layers: [new GridCellLayer(this.layerSettings.gridCellLayer), new TextLayer(this.layerSettings.textLayer)] })
      } else if (updatedSettings.type === 'lighting') {
        if (s.advancedLighting === true) {
          // Only build new lights when advanced light is activated. Probably not necessary but I speculate on performance advantages with this approach.
          const ambient = new AmbientLight({
            color: [255, 255, 255],
            intensity: s.ambientLight
          })
          const directionalLight1 = new DirectionalLight({
            color: [255, 255, 255],
            direction: [this.highestValue / 2, 5, 3000],
            intensity: s.directionalLight1
          })
          const directionalLight2 = new DirectionalLight({
            color: [255, 255, 255],
            position: [this.highestValue / 4, 0.1, 1000],
            intensity: s.directionalLight2
          })
          this.deck.setProps({
            effects: [
              new LightingEffect({
                ambient,
                directionalLight1,
                directionalLight2
              })
            ]
          })
        } else {
          this.deck.setProps({ effects: [] })
        }
      }
      this.$emit('longLoadingFinished')
    },
    fetchData: function (url) {
      var payload = new FormData()
      payload.append('url', JSON.stringify(this.$route.query.config))
      axios
        .post(url, payload)
        .then(res => {
          [
            this.layerSettings.gridCellLayer.data,
            this.layerSettings.textLayer.data,
            this.highestValue,
            this.lowestValue
          ] = this.processJsonData(res.data)
        })
        .catch(error => {
          console.log(error)
        })
    },
    processJsonData: function (json) {
      // This could be moved to the python backend for performace reasons.
      var gridCellLayerData = []
      var textLayerData = []
      var columns = Object.keys(json[0])
      var lowestValue = 0
      var highestValue = 0
      var lastPrefix
      var columnName
      var columnCoordinate = 0
      for (var columnIndex = 0; columnIndex < columns.length; columnIndex++) {
        if (columns[columnIndex].startsWith('(')) {
          var splitIndex = columns[columnIndex].indexOf(') ')
          var prefix = columns[columnIndex].slice(0, splitIndex + 1)
          if (prefix !== lastPrefix) {
            lastPrefix = prefix
            columnCoordinate += 1.4
          } else {
            columnCoordinate++
          }
          columnName = columns[columnIndex].slice(splitIndex + 2)
        } else {
          columnName = columns[columnIndex]
        }
        var scaledColumnCoordinate = columnCoordinate / 140 // Only calculate x coordinate when the column changes.
        for (var rowIndex = 0; rowIndex < json.length; rowIndex++) {
          var gridCellLayerCell = {
            COLUMN: columnName,
            COORDINATES: [rowIndex / 140, scaledColumnCoordinate],
            ROW: json[rowIndex][columns[0]],
            VALUE: json[rowIndex][columns[columnIndex]]
          }
          gridCellLayerData.push(gridCellLayerCell)
          if (
            gridCellLayerCell.VALUE > highestValue &&
            gridCellLayerCell.VALUE !== Infinity &&
            gridCellLayerCell.VALUE !== -Infinity
          ) {
            highestValue = gridCellLayerCell.VALUE
          }
          if (
            gridCellLayerCell.VALUE < lowestValue &&
            gridCellLayerCell.VALUE !== -Infinity &&
            gridCellLayerCell.VALUE !== Infinity
          ) {
            lowestValue = gridCellLayerCell.VALUE
          }
          if (columnIndex === 0) {
            textLayerData.push({
              COORDINATES: [gridCellLayerCell.COORDINATES[0] + this.constants.textMarginTop, this.constants.textMarginRight],
              VALUE: gridCellLayerCell.ROW
            })
          }
        }
      }
      return [gridCellLayerData, textLayerData, highestValue, lowestValue]
    },
    getTooltip: function ({ object }) {
      if (!object) {
        return null
      }
      const column = object.COLUMN
      const row = object.ROW
      const count = object.VALUE
      return {
        html: `\
        ${column}<br>
        ${row}<br>
        <strong>${count}</strong>`
        // style: {
        //   backgroundColor: '#000',
        //   margin: '0'
        // }
      }
      // Below is an example for a more advanced tooltip format according to: https://github.com/visgl/deck.gl/blob/8.3-release/examples/website/3d-heatmap/app.js
      // const lat = object.COORDINATES[1]
      // const lng = object.COORDINATES[0]
      // return `\
      //   latitude: ${Number.isFinite(lat) ? lat.toFixed(6) : ''}
      //   longitude: ${Number.isFinite(lng) ? lng.toFixed(6) : ''}
      //   ${count} Accidents`
    }
  }
}
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
.settings_menu {
  top: 10px;
  left: 10px;
}
.camera_menu {
  top: 10px;
  right: 10px;
}
.menu_c {
  position: absolute;
  z-index: 1000;
}
</style>
