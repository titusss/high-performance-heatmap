<!-- App / deckglCanvas / mainMenu / settingsMenu -->
<template>
  <div class="menu" v-if="settingsTemplate">
    <div
      v-for="settingsMode in settingsTemplate"
      :key="settingsMode.id"
      class="mb-4"
    >
      <b-button
        v-if="settingsMode.id !== 'generalSettings'"
        variant="link"
        class="header"
        v-b-toggle="settingsMode.id"
        size="sm"
        ><b-icon
          icon="chevron-down"
          style="padding-bottom: 3px;"
        ></b-icon
        ><span>{{ settingsMode.label }}</span></b-button
      >
      <b-collapse
        :id="settingsMode.id"
        :visible="settingsMode.visible"
        class="mt-2"
      >
        <b-form-group
          v-for="block in settingsMode.settings"
          :key="block.id"
          size="sm"
          label-align="left"
          :id="block.label"
          :label="block.label"
          class="mb-3"
        >
          <b-form-group
            label-align="left"
            :label-cols="6"
            v-for="input in block.inputs"
            :key="input.label"
            :label="input.label"
            :label-for="input.id"
            label-class="input_label"
            class="input_group_custom"
          >
            <b-form-input
              v-if="input.type === 'range' || input.type === 'dropdown'"
              v-model="localSettings[input.propertyType][input.id]"
              :type="input.type"
              :step="input.step"
              :min="input.min"
              :max="input.max"
              :id="input.id"
              :disabled="
                input.valueDependencyId
                  ? !localSettings[input.propertyType][input.valueDependencyId]
                  : false
              "
            ></b-form-input>
            <b-form-checkbox
              v-else-if="input.type === 'checkbox'"
              v-model="localSettings[input.propertyType][input.id]"
              :type="input.type"
              :id="input.id"
              :disabled="
                input.valueDependencyId
                  ? !localSettings[input.propertyType][input.valueDependencyId]
                  : false
              "
            ></b-form-checkbox>
            <b-dropdown
              class="dropdown-gradient"
              variant="link"
              size="sm"
              v-model="localSettings[input.propertyType][input.id]"
              v-else-if="input.type === 'dropdownGradient'"
              :id="input.id"
              :disabled="
                input.valueDependencyId
                  ? !localSettings[input.propertyType][input.valueDependencyId]
                  : false
              "
              ><template v-slot:button-content>
                {{ localSettings[input.propertyType][input.id].label }}
                <div class="gradient-preview" id="selected-gradient-preview"
                  :style="getColorGradientCss( localSettings[input.propertyType][input.id].label )">
                </div>
              </template>
              <b-dropdown-item-button
                v-for="gradient in input.options"
                :key="gradient"
                @click="localSettings[input.propertyType][input.id].label = gradient,
                localSettings[input.propertyType][input.id].value = gradient">
                <span class="gradient-label">{{gradient}}</span>
                <div class="gradient-preview"
                  :style="getColorGradientCss( gradient )">
                </div>
              </b-dropdown-item-button>
            </b-dropdown>
          </b-form-group>
        </b-form-group>
      </b-collapse>
    </div>
  </div>
</template>

<script>
import chroma from 'chroma-js';

export default {
  props: {
    settings: Object,
    settingsTemplate: Object,
  },
  watch: {
    'settings.layer': {
      handler() {
        this.$emit('settings-changed', { type: 'layer', settings: this.localSettings.layer });
      },
      deep: true,
    },
    'localSettings.material': {
      handler() {
        this.$emit('settings-changed', { type: 'material', settings: this.localSettings.material });
      },
      deep: true,
    },
    'localSettings.lighting': {
      handler() {
        this.$emit('settings-changed', { type: 'lighting', settings: this.localSettings.lighting });
      },
      deep: true,
    },
  },
  data() {
    return {
      localSettings: this.settings,
    };
  },
  created() {
    console.log(this.settings);
    this.$emit('settings-changed', { type: 'layer', settings: this.localSettings.layer });
  },
  methods: {
    getColorGradientCss(gradientName) {
    // Maybe generate an Object when component is created() to prevent render on call.
      const gradientSteps = 10;
      const colorArray = [];
      const colorGradient = chroma
        .scale(gradientName)
        .domain([0, gradientSteps]);
      for (let i = 0; i < gradientSteps; i += 1) {
        colorArray.push(colorGradient(i));
      }
      return `background-image: linear-gradient(to right, ${colorArray})`;
    },
  },
};
</script>

<style>
.menu {
  background-color: #fff;
  width: 369px;
  padding: 20px 40px 10px 40px;
  box-shadow: 10px 30px 60px rgba(0, 0, 0, 0.05);
  border-radius: 5px;
  font-size: 14px;
}
legend {
  font-weight: 600;
}
.input_label {
  justify-content: left !important;
}
label {
  padding: 2px 5px 2px 5px !important;
}
.bv-no-focus-ring > input {
  height: 100% !important;
}
.custom-control {
  text-align: left !important;
}
.input_group_custom {
  margin-bottom: 0px !important;
}
.header {
  color: #2c3e50 !important;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 400;
  text-decoration: none !important;
  font-size: 12px !important;
}
.header:hover {
  color: #308ae4 !important;
}
.no_rotation {
  transform: rotate(0);
}
.rotate_down {
  transform: rotate(90);
}
.dropdown-gradient {
  float: left;
  margin-left: -5px;
  border-bottom: 2px solid #d6d8db;
}
.dropdown-gradient>button {
  text-decoration: none !important;
  color: #2c3e50;
  padding: 0px !important;
  display: flex;
  justify-content: center;
  align-items: center;
}
.gradient-label {
  margin-right: .25rem;
}
.dropdown-item {
  display: flex !important;
  justify-content: center;
  align-items: center;
  padding: .25rem 1.5rem !important;
}
.gradient-preview {
  width: 3rem;
  height: 1.5rem;
  border-radius: .75rem;
  margin-left: auto;
}
#selected-gradient-preview {
  margin: .25rem;
}
.form-row {
  align-items: center !important;
}
.dropdown-menu.show {
  display: grid !important;
  grid-template-columns: repeat(3, 1fr) !important;
}
</style>
