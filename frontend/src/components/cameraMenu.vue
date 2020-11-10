<!-- App / deckglCanvas / cameraMenu -->
<template>
  <div class="main_parent">
    <div class="buttons_background">
      <div
        @click="$emit('active-camera-selected', option)"
        class="option_button"
        :class="{ option_button_active: activeCamera === option.id }"
        v-for="option in cameraOptions"
        :key="option.id"
      >
        <img class="option_icon" :src="require(`@/assets/${option.id}.svg`)" />
      </div>
    </div>
    <label
      :class="{ label_active: activeCamera === option.id }"
      v-for="option in cameraOptions"
      :key="option.id"
      >{{ option.id }}</label
    >
  </div>
</template>

<script>
export default {
  props: {
    activeCamera: String,
  },
  data() {
    return {
      cameraOptions: [
        {
          id: '3D',
          viewState: {
            pitch: 40,
            bearing: -40,
          },
          layerSettings: {
            gridCellLayer: {
              extruded: true,
            },
          },
        },
        {
          id: 'Top',
          viewState: {
            pitch: 0,
            bearing: -90,
          },
          layerSettings: {
            gridCellLayer: {
              extruded: false,
            },
          },
        },
        {
          id: 'Side',
          viewState: {
            pitch: 90,
            bearing: 0,
          },
          layerSettings: {
            gridCellLayer: {
              extruded: true,
            },
          },
        },
        {
          id: 'Front',
          viewState: {
            pitch: 90,
            bearing: 90,
          },
          layerSettings: {
            gridCellLayer: {
              extruded: true,
            },
          },
        },
      ],
    };
  },
};
</script>

<style scoped>
.option_button {
  padding: 10px 16px 10px 16px;
  background-color: #fff;
  border-radius: 5px;
  grid-area: 1 / auto / 2 / auto;
  cursor: pointer;
  transition: background-color 200ms ease-out;
}
.main_parent {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(2, auto);
  grid-row-gap: 10px;
}
label {
  font-size: 14px;
  grid-area: 2 / auto / auto / auto;
}
.buttons_background {
  grid-area: 1 / 1 / 2 / 7;
  background-color: #fff;
  box-shadow: 3px 6px 16px #0000001c;
  border-radius: 5px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
}
.label_active {
  font-weight: 600;
}
.option_button_active {
  background-color: #1c1c29 !important;
  border-radius: 5px;
}
.option_button_active>img {
  filter: saturate(0) brightness(1.8);
}
.option_button > img {
  transition: transform 350ms cubic-bezier(0.36, 1.59, 0.66, 1);
}
.option_button:hover > img {
  transform: scale(1.3);
}
</style>
