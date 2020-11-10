<template>
  <div class="menu">
    <div class="mb-4">
      <div class="header mt-3 mb-2">Download Top View as SVG</div>
      <!-- <label>Export the 2D top view of the heatmap.</label> -->
      <b-button block variant="dark" size="sm" @click="exportCanvasSvg">
        <!-- <img :src="require(`@/assets/exportImage.svg`)"> Download SVG -->
        <b-icon icon="download" aria-hidden="true"></b-icon> SVG Heatmap
      </b-button>
      <div class="header mt-3 mb-2">Download Current View as PNG</div>
      <b-button block variant="dark" size="sm">
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
  methods: {
    exportCanvasSvg() {
      const domElement = document.getElementById('export_svg');
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      const svgNS = svg.namespaceURI;
      svg.setAttribute('id', 'downloadble_svg');
      svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
      const size = this.layerSettings.cellSize / 50;
      for (
        let i = 0;
        i < this.layerSettings.data.length;
        i += 1
      ) {
        const rect = document.createElementNS(svgNS, 'rect');
        rect.setAttribute(
          'x',
          this.layerSettings.data[i].COORDINATES[1] * 2220,
        );
        rect.setAttribute(
          'y',
          this.layerSettings.data[i].COORDINATES[0] * 2220,
        );
        rect.setAttribute('width', size);
        rect.setAttribute('height', size);
        rect.setAttribute(
          'fill',
          this.colorGradient(
            this.layerSettings.data[i].VALUE,
          ).hex(),
        );
        svg.appendChild(rect);
      }
      svg.setAttribute(
        'width',
        this.layerSettings.data[
          this.layerSettings.data.length - 1
        ].COORDINATES[1]
          * 2220
          + this.layerSettings.cellSize / 50,
      );
      svg.setAttribute(
        'height',
        this.layerSettings.data[
          this.layerSettings.data.length - 1
        ].COORDINATES[0]
          * 2220
          + this.layerSettings.cellSize / 50,
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
</style>
