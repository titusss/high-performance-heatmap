<template>
  <div>
    <div>
      <label for="range-1">Example range with min and max</label>
      <b-form-input
        id="range-1"
        v-model="settings.elevationScale"
        type="range"
        min="0"
        max="500"
      ></b-form-input>
      <div class="mt-2">Value: {{ settings.elevationScale }}</div>
    </div>
    <div class="deck-container" v-if="settings.elevationScale">
      <canvas id="deck-canvas" ref="canvas"></canvas>
    </div>
  </div>
</template>

<script>
import { Deck } from '@deck.gl/core'
import { GridCellLayer } from '@deck.gl/layers'
import axios from 'axios'
export default {
  data () {
    return {
      url: 'http://[::]:8000/test-dict-index.json',
      data: null,
      highestValue: null,
      lowestValue: null,
      settings: {
        elevationScale: 500
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
  computed: {
    getSettings () {
      return this.settings.elevationScale
    },
    getLayers () {
      const gridLayer = new GridCellLayer({
        id: 'grid-cell-layer',
        data: this.data,
        elevationScale: 400,
        extruded: true,
        cellSize: this.settings.elevationScale,
        getPosition: d => d.COORDINATES,
        getFillColor: d => [255, 255, 0, 255],
        getElevation: d => d.VALUE
      })
      return [gridLayer]
    }
  },
  watch: {
    // whenever the layer data is changed and new layers are created,
    // rerender the layers
    getLayers (layers) {
      this.renderLayers(layers)
    }
  },
  methods: {
    renderLayers (layers) {
      // setting the layers to deck.gl props
      this.deck.setProps({
        layers
      })
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
      var highestValue
      var lowestValue
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
</style>
