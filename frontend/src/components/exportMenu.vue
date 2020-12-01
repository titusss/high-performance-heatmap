<template>
  <div class="menu">
    <a id="canvas-png-link"></a>
    <div class="mb-4">
      <div class="header mt-3 mb-2">Download Top View as SVG</div>
      <!-- <label>Export the 2D top view of the heatmap.</label> -->
        <b-form inline class="mb-1 custom-b-form">
          <b-form-group label="Export text" label-for="checkbox-1">
          <b-form-checkbox
          id="checkbox-1"
          v-model="showText"
          name="checkbox-1"
          value="true"
          unchecked-value="false"
        />
         </b-form-group>
        </b-form>
      <b-button block variant="dark" size="sm" @click="exportCanvasSvg">
        <!-- <img :src="require(`@/assets/exportImage.svg`)"> Download SVG -->
        <b-icon icon="download" aria-hidden="true"></b-icon> SVG Heatmap
      </b-button>
      <div class="header mt-3 mb-2">Download Current View as PNG</div>
      <b-button id="btn-download" block variant="dark" size="sm" @click="$emit('take-screenshot')">
        <!-- <img :src="require(`@/assets/exportImage.svg`)"> Download SVG -->
        <b-icon icon="download" aria-hidden="true"></b-icon> PNG Current View
      </b-button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    layerSettings: Object,
    colorGradient: Function,
  },
  data() {
    return {
      xMargin: undefined,
      yMargin: undefined,
      showText: 'true',
    };
  },
  methods: {
    exportCanvasSvg() {
      // This needs to be slimmed down.
      const domElement = document.getElementById('export_svg');
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      const svgNS = svg.namespaceURI;
      svg.setAttribute('id', 'downloadble_svg');
      svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
      const size = this.layerSettings.gridCellLayer.cellSize / 50;
      const cellGroup = document.createElementNS(svgNS, 'g');
      cellGroup.setAttribute('style', 'font-size: 11px;font-family: HelveticaNeue, Helvetica Neue;text-align: right;');
      if (this.showText === 'true') {
        this.xMargin = 80;
        this.yMargin = 100;
        const columnGroup = document.createElementNS(svgNS, 'g');
        const rowGroup = document.createElementNS(svgNS, 'g');
        rowGroup.setAttribute('style', 'font-size: 11px;font-family: HelveticaNeue, Helvetica Neue;text-align: right;');
        columnGroup.setAttribute('style', 'font-size: 11px;font-family: HelveticaNeue, Helvetica Neue;');
        svg.appendChild(rowGroup);
        svg.appendChild(columnGroup);
        for (let i = 0; i < this.layerSettings.columnTextLayer.data.length; i += 1) {
          const columnText = document.createElementNS(svgNS, 'text');
          const columnTextNode = document
            .createTextNode(this.layerSettings.columnTextLayer.data[i].VALUE);
          columnText.setAttribute('transform', `rotate(-90) translate(-90, ${this.layerSettings.columnTextLayer.data[i].COORDINATES[1] * 2220 + this.xMargin + 4})`);
          columnText.appendChild(columnTextNode);
          columnGroup.appendChild(columnText);
        }
        for (let j = 0; j < this.layerSettings.rowTextLayer.data.length; j += 1) {
          const rowText = document.createElementNS(svgNS, 'text');
          const rowTextNode = document
            .createTextNode(this.layerSettings.rowTextLayer.data[j].VALUE);
          rowText.setAttribute('x', 0);
          rowText.setAttribute('y', this.layerSettings.rowTextLayer.data[j].COORDINATES[0] * 2220 + this.yMargin + 4);
          rowText.appendChild(rowTextNode);
          rowGroup.appendChild(rowText);
        }
      } else {
        this.xMargin = 0;
        this.yMargin = 0;
      }
      for (let k = 1; k < this.layerSettings.gridCellLayer.data.length; k += 1) {
        let orientation;
        const rect = document.createElementNS(svgNS, 'rect');
        rect.setAttribute(
          'x',
          this.layerSettings.gridCellLayer.data[k].COORDINATES[1] * 2220 + this.xMargin,
        );
        rect.setAttribute(
          'y',
          this.layerSettings.gridCellLayer.data[k].COORDINATES[0] * 2220 + this.yMargin,
        );
        rect.setAttribute('width', size);
        rect.setAttribute('height', size);
        // Following lines are heavy on performance. Maybe check for lowest_value < 0?
        if (!this.layerSettings.gridCellLayer.data[k].ORIENTATION) {
          orientation = 1;
        } else {
          orientation = this.layerSettings.gridCellLayer.data[k].ORIENTATION;
        }
        rect.setAttribute(
          'fill',
          this.colorGradient(this.layerSettings.gridCellLayer.data[k].VALUE
            * orientation).hex(),
        );
        cellGroup.appendChild(rect);
      }
      for (let l = 1; l < this.layerSettings.textCellLayer.data.length; l += 1) {
        if (this.layerSettings.textCellLayer.data[l].VALUE) {
          const text = document.createElementNS(svgNS, 'text');
          const textNode = document
            .createTextNode(this.layerSettings.textCellLayer.data[l].VALUE);
          text.setAttribute('y', this.layerSettings.textCellLayer.data[l].COORDINATES[0] * 2220 + this.yMargin);
          text.setAttribute('style', `font-size: ${32 / (this.layerSettings.textCellLayer.data[l].VALUE.length + 2.5)}px`);
          // The following is a dumb quick-fix and should be replaced.
          // Calculates the x position based on string length to center it.
          text.setAttribute('x', this.layerSettings.textCellLayer.data[l].COORDINATES[1] * 2220 + this.xMargin - 8 + 4 / this.layerSettings.textCellLayer.data[l].VALUE.length);
          text.appendChild(textNode);
          cellGroup.appendChild(text);
        }
      }
      svg.appendChild(cellGroup);
      svg.setAttribute(
        'width',
        this.layerSettings.gridCellLayer.data[this.layerSettings.gridCellLayer.data.length - 1]
          .COORDINATES[1]
          * 2220
          + this.layerSettings.gridCellLayer.cellSize / 50
          + 100,
      );
      svg.setAttribute(
        'height',
        this.layerSettings.gridCellLayer.data[this.layerSettings.gridCellLayer.data.length - 1]
          .COORDINATES[0]
          * 2220
          + this.layerSettings.gridCellLayer.cellSize / 50
          + 100,
      );
      domElement.appendChild(svg);
      const svgData = document.getElementById('downloadble_svg').outerHTML;
      domElement.removeChild(svg);
      const svgBlob = new Blob([svgData], {
        type: 'image/svg+xml;charset=utf-8',
      });
      const svgUrl = URL.createObjectURL(svgBlob);
      const downloadLink = document.createElement('a');
      downloadLink.href = svgUrl;
      downloadLink.download = 'newesttree.svg';
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
    },
  },
};
</script>

<style scoped>
svg {
  margin-right: 0.25rem;
}
.menu {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background-color: #fff;
  width: 369px;
  padding: 20px 40px 10px 40px;
  box-shadow: 10px 30px 60px rgba(0, 0, 0, 0.08);
  border-radius: 5px;
  font-size: 14px;
}
legend {
  font-weight: 600;
}
button {
  background-color: #1c1d29;
  padding: 0.5rem;
}
.header {
  color: #2c3e50 !important;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 400;
  text-decoration: none !important;
  font-size: 12px !important;
}
.form-group{
  margin: auto;
  font-family:
    "Space Grotesk", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
}
</style>
