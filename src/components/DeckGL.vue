<template>
  <div>
    <div class="deck-container">
      <canvas id="deck-canvas" ref="canvas"></canvas>
    </div>
    <settingsMenu v-if="data" class="settings_menu" @settingsChanged="updateSettings"/>
  </div>
</template>

<script>
import { Deck, LightingEffect, AmbientLight, PointLight } from '@deck.gl/core'
import { GridCellLayer } from '@deck.gl/layers'
import axios from 'axios'
import settingsMenu from '@/components/settingsMenu.vue'
import chroma from 'chroma-js'
export default {
  components: {
    settingsMenu
  },
  data () {
    return {
      // url: 'http://[::]:8000/test-dict-index.json',
      url:
        'https://raw.githubusercontent.com/chinapwn/high-performance-heatmap/master/src/assets/test-dict-index.json',
      data: null,
      highestValue: null,
      lowestValue: null,
      colorGradient: null,
      colorGradientPreset: null,
      advancedLighting: false,
      lights: {
        ambientLight: {
          color: [255, 255, 255],
          intensity: 1
        },
        pointLight1: {
          color: [255, 255, 255],
          intensity: 0.8,
          position: [-0.144528, 49.739968, 80000]
        },
        pointLight2: {
          color: [255, 255, 255],
          intensity: 0.8,
          position: [-3.807751, 54.104682, 8000]
        }
      },
      layerSettings: {
        gridCellLayer: {
          id: 'grid-cell-layer',
          getPosition: d => d.COORDINATES,
          getElevation: d => d.VALUE,
          getFillColor: d => this.colorGradient(d.VALUE).rgb(),
          updateTriggers: { getFillColor: this.colorGradientPreset }
        }
      },
      viewState: {
        latitude: 0,
        longitude: 0.007,
        zoom: 11,
        pitch: 40,
        bearing: 10
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
    this.fetchData(this.url)
    this.deck = null
  },
  mounted () {
    this.deck = new Deck({
      canvas: this.$refs.canvas,
      initialViewState: this.viewState,
      controller: true
    })
    // this.deck.layerManager.layers[0].props.elevationScale = 10
  },
  methods: {
    updateSettings (updatedSettings) {
      const s = updatedSettings.settings
      if (updatedSettings.type === 'layer') {
        // This isn't optimal as selected properties are defined in this update function.
        const settings = Object.assign(s, this.layerSettings.gridCellLayer)
        settings.data = this.data
        if (this.colorGradientPreset !== s.gradientPreset.value) {
          this.colorGradientPreset = s.gradientPreset.value
          this.colorGradient = chroma
            .scale(this.colorGradientPreset)
            .domain([this.lowestValue / 100, this.highestValue / 100])
          settings.updateTriggers = { getFillColor: this.colorGradientPreset }
        }
        settings.elevationScale = Number(s.elevationScale) // This property is converted to string by Vue.js
        this.deck.setProps({ layers: [new GridCellLayer(settings)] })
      } else if (updatedSettings.type === 'lighting') {
        if (s.advancedLighting === true) {
          const ambient = new AmbientLight({
            color: [255, 255, 255],
            intensity: s.ambientLight
          })
          const pointLight1 = new PointLight({
            color: [255, 255, 255],
            position: [0, 0, 30],
            intensity: s.pointLight1
          })
          const pointLight2 = new PointLight({
            color: [255, 255, 255],
            position: [1, 2, 500],
            intensity: s.pointLight2
          })
          this.deck.setProps({
            effects: [new LightingEffect({ ambient, pointLight1, pointLight2 })]
          })
        } else {
          this.deck.setProps({ effects: [] })
        }
      }
    },
    fetchData: function (url) {
      axios.get(url).then(res => {
        [this.data, this.highestValue, this.lowestValue] = this.processJsonData(
          res.data
        )
      })
    },
    processJsonData: function (json) {
      var data = []
      var rows = Object.keys(json)
      var columns = Object.keys(json[rows[0]])
      var highestValue = json[rows[0]][columns[0]]
      var lowestValue = json[rows[0]][columns[0]]
      for (var rowIndex = 0; rowIndex < rows.length; rowIndex++) {
        for (var columnIndex = 1; columnIndex < columns.length; columnIndex++) {
          if (
            columns[columnIndex] !== 'start' &&
            columns[columnIndex] !== 'end' &&
            columns[columnIndex] !== 'strand'
          ) {
            var cell = {
              COORDINATES: [],
              VALUE: 0
            }
            cell.COORDINATES.push(rowIndex / 140)
            cell.COORDINATES.push(columnIndex / 140)
            cell.VALUE =
              Math.log(json[rows[rowIndex]][columns[columnIndex]]) /
              Math.log(2)
            // cell.VALUE = json[rows[rowIndex]][columns[columnIndex]];
            data.push(cell)
            if (cell.VALUE > highestValue) {
              highestValue = cell.VALUE
            }
            if (cell.VALUE < lowestValue) {
              if (cell.VALUE < 0) {
                lowestValue = 1
              } else {
                lowestValue = cell.VALUE
              }
            }
          }
        }
      }
      return [data, highestValue, lowestValue]
    }
  }
}
</script>

<style>
.deck-container {
  width: 100vw;
  height: 80vh;
  position: relative;
}
#deckgl-overlay {
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
}
.settings_menu {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 1000;
}
</style>
