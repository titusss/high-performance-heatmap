<!-- App / deckglCanvas / mainMenu -->
<template>
  <div>
    <div class="buttons_background">
      <div
        @click="setActiveOption(option.id)"
        class="option_button"
        :class="{ option_button_active: activeOptionId === option.id }"
        v-for="option in options"
        :key="option.id"
      >
        <img class="option_icon" :src="require(`@/assets/${option.id}.svg`)" />
      </div>
    </div>
    <b-collapse
      v-for="option in options"
      :key="option.id"
      :visible="activeOptionId === option.id"
    >
      <settingsMenu
        v-if="option.id === 'deckglSettings'"
        @settings-changed="$emit('settings-changed', $event)"
        :settings="settings"
        :settingsTemplate="settingsTemplate"
      />
      <exportMenu
        v-else-if="option.id === 'exportImage'"
        :layerSettings="layerSettings"
        :colorGradient="colorGradient"
      />
    </b-collapse>
  </div>
</template>

<script>
import settingsMenu from './settingsMenu.vue';
import exportMenu from './exportMenu.vue';

export default {
  components: {
    settingsMenu,
    exportMenu,
  },
  props: {
    settings: Object,
    settingsTemplate: Object,
    layerSettings: Object,
    colorGradient: Function,
  },
  data() {
    return {
      options: [
        {
          id: 'goHome',
          label: 'Home',
        },
        {
          id: 'deckglSettings',
          label: 'Settings',
        },
        {
          id: 'exportImage',
          label: 'Export Image',
        },
      ],
      activeOptionId: null,
    };
  },
  methods: {
    setActiveOption(id) {
      if (this.activeOptionId !== id) {
        this.activeOptionId = id;
      } else {
        this.activeOptionId = null;
      }
    },
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
label {
  font-size: 14px;
  grid-area: 2 / auto / auto / auto;
}
.buttons_background {
  position: relative;
  z-index: 1100;
  grid-area: 1 / 1 / 2 / 7;
  background-color: #fff;
  box-shadow: 3px 6px 16px #0000001c;
  border-radius: 5px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  width: fit-content;
  margin-bottom: 5px;
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
