<template>
  <div>
    <div class="deck-container">
      <canvas id="deck-canvas" ref="canvas"></canvas>
    </div>
    <settingsMenu v-if="data" class="settings_menu" @settingsChanged="updateSettings"/>
  </div>
</template>

<script>
import { Deck } from '@deck.gl/core'
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
      url: 'https://raw.githubusercontent.com/chinapwn/high-performance-heatmap/master/src/assets/test-dict-index.json',
      data: null,
      highestValue: null,
      lowestValue: null,
      elevationScale: 20,
      ready: null,
      layerSettings: {
        gridCellLayer: {
          id: 'grid-cell-layer',
          getPosition: d => d.COORDINATES,
          getElevation: d => d.VALUE
          // scale = chroma.scale(schemeNames.diverging[1]).domain([min, max]);
        }
      },
      cellSize: 200,
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
    this.ready = true
    // this.deck.layerManager.layers[0].props.elevationScale = 10
  },
  methods: {
    updateSettings (updatedSettings) {
      const settings = Object.assign(updatedSettings, this.layerSettings.gridCellLayer)
      settings.data = this.data
      settings.elevationScale = Number(updatedSettings.elevationScale) // This property is converted to string by Vue.js
      const colorGradient = chroma.scale(updatedSettings.gradientPreset.value).domain([this.lowestValue, this.highestValue / 100])
      settings.getFillColor = d => colorGradient(d.VALUE).rgb()
      settings.updateTriggers = { getFillColor: [colorGradient] }
      this.deck.setProps({ layers: [new GridCellLayer(settings)] })
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
      console.log(highestValue)
      console.log(data)
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
