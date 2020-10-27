<template>
  <div>
    <div class="deck-container">
      <canvas id="deck-canvas" ref="canvas"></canvas>
    </div>
    <settingsMenu
      v-if="data"
      class="settings_menu"
      @settingsChanged="updateSettings"
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
      // backendUrl: 'http://127.0.0.1:5000',
      backendUrl: 'https://hp-heatmap-backend-44nub6ij6q-ez.a.run.app',
      data: null,
      highestValue: null,
      lowestValue: null,
      colorGradient: null,
      colorGradientPreset: null,
      advancedLighting: false,
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
      initialViewState: this.viewState,
      controller: true,
      getTooltip: this.getTooltip
    })
    // this.deck.layerManager.layers[0].props.elevationScale = 10
  },
  methods: {
    updateSettings (updatedSettings) {
      const s = updatedSettings.settings
      // It might be useful to use a switch case instead, if the possible conditions grow beyond 5 items.
      if (updatedSettings.type === 'layer') {
        const settings = Object.assign(s, this.layerSettings.gridCellLayer)
        settings.data = this.data
        if (this.colorGradientPreset !== s.gradientPreset.value) {
          this.colorGradientPreset = s.gradientPreset.value
          this.colorGradient = chroma
            .scale(this.colorGradientPreset)
            .domain([this.lowestValue, this.highestValue])
          settings.updateTriggers = { getFillColor: this.colorGradientPreset }
        }
        settings.elevationScale = Number(s.elevationScale) // This is necessary because Vue.js converts the property to a string.
        this.deck.setProps({ layers: [new GridCellLayer(settings)] })
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
            this.data,
            this.highestValue,
            this.lowestValue
          ] = this.processJsonData(res.data)
          console.log(res)
        })
        .catch(error => {
          console.log(error)
        })
    },
    processJsonData: function (json) {
      // This could be moved to the python backend for performace reasons
      var data = []
      var rows = Object.keys(json)
      var columns = Object.keys(json[rows[0]])
      var lowestValue = json[rows[0]][columns[4]]
      var highestValue = json[rows[0]][columns[4]]
      var lastPrefix
      var columnName
      for (var rowIndex = 0; rowIndex < rows.length; rowIndex++) {
        var columnCoordinate = 0
        for (var columnIndex = 0; columnIndex < columns.length; columnIndex++) {
          var cell = {
            COORDINATES: [],
            VALUE: 0
          }
          if (columns[columnIndex].startsWith('(')) {
            var splitIndex = columns[columnIndex].indexOf(') ')
            var prefix = columns[columnIndex].slice(0, splitIndex + 1)
            if (prefix !== lastPrefix) {
              lastPrefix = prefix
              columnCoordinate += 1.3
            } else {
              columnCoordinate++
            }
            columnName = columns[columnIndex].slice(splitIndex + 2)
          } else {
            columnName = columns[columnIndex]
          }
          cell.COORDINATES.push(rowIndex / 140)
          cell.COORDINATES.push(columnCoordinate / 140)
          cell.COLUMN = columnName
          cell.ROW = rows[rowIndex]
          // cell.VALUE =
          //   Math.log(json[rows[rowIndex]][columns[columnIndex]]) /
          //   Math.log(2)
          cell.VALUE = json[rows[rowIndex]][columns[columnIndex]]
          data.push(cell)
          if (
            cell.VALUE > highestValue &&
            cell.VALUE !== Infinity &&
            cell.VALUE !== -Infinity
          ) {
            highestValue = cell.VALUE
          }
          if (
            cell.VALUE < lowestValue &&
            cell.VALUE !== -Infinity &&
            cell.VALUE !== Infinity
          ) {
            lowestValue = cell.VALUE
          }
        }
      }
      console.log(lowestValue, highestValue)
      return [data, highestValue, lowestValue]
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

<style>
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
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 1000;
}
</style>
