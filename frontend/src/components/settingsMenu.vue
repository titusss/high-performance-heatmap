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
          :key="block.label"
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
            :key="input.id"
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
              v-b-tooltip.hover
              :title="localSettings[input.propertyType][input.id]"
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
                  ? !localSettings[input.propertyType][input.valueDependencyId] === input.condition
                  : false
              "
              ><template v-slot:button-content>
                {{ localSettings[input.propertyType][input.id].label }}
                <div class="gradient-preview" id="selected-gradient-preview"
                  :style="getColorGradientCss(
                    localSettings[input.propertyType][input.id].label,
                    localSettings[input.propertyType][input.id].domain
                  )">
                </div>
              </template>
              <div class="gradient-slider-parent">
              <!-- <label for="range-1">Example range with min and max</label> -->
              <vue-slider
                :style="getColorGradientCss(
                  localSettings[input.propertyType][input.id].label,
                  localSettings[input.propertyType][input.id].domain
                )"
                :min="minValue"
                :max="maxValue"
                height="1.5rem"
                :lazy="false"
                :tooltip-placement="'bottom'"
                tooltip="always"
                v-model="localSettings[input.propertyType][input.id].domain"
                :contained="true"
                :order="true"
                :useKeyboard="false"
                :marks="[minMaxValues[0], input.min, input.max, minMaxValues[1]]"
                :interval="gradientSliderInterval"
                >
                 <template v-slot:tooltip="{ index }">
                  <div class="gradient-value-input">
                    <!-- Add the following lines to the b-form-input props
                    to adjust the width of the form based on input length
                     :style="
                      `width: ${
                        String(localSettings[input.propertyType][input.id].domain[index]).length
                        * 10
                      }px`
                    " -->
                    <b-form-input size="sm" type="number"
                    :min="minMaxValues[0]" :max="minMaxValues[1]" v-model="
                    localSettings[input.propertyType][input.id].domain[index]
                    "></b-form-input>
                  </div>
                </template>
              </vue-slider>
              </div>
              <div class="gradient-overview">
              <b-dropdown-item-button
                v-for="gradient in input.options"
                :id="input.id"
                :key="gradient"
                @click="localSettings[input.propertyType][input.id].label = gradient,
                localSettings[input.propertyType][input.id].value = gradient">
                <span class="gradient-label">{{gradient}}</span>
                <div class="gradient-preview"
                  :style="getColorGradientCss( gradient, [minValue,
                  (maxValue - minValue) / 2 + minValue, maxValue] )">
                </div>
              </b-dropdown-item-button>
              </div>
            </b-dropdown>
          </b-form-group>
        </b-form-group>
      </b-collapse>
    </div>
  </div>
</template>

<script>
import chroma from 'chroma-js';
import VueSlider from 'vue-slider-component';
import 'vue-slider-component/theme/default.css';

export default {
  components: {
    VueSlider,
  },
  computed: {
    minValue() {
      return Math.floor(this.minMaxValues[0]);
    },
    maxValue() {
      return Math.ceil(this.minMaxValues[1]);
    },
  },
  props: {
    settings: Object,
    settingsTemplate: Object,
    minMaxValues: Array,
  },
  watch: {
    'settings.layer': {
      handler() {
        this.$emit('settings-changed', { type: 'layer', settings: this.localSettings.layer });
      },
      deep: true,
    },
    'settings.gradient': {
      handler() {
        this.$emit('settings-changed', { type: 'gradient', settings: this.localSettings.gradient });
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
      gradientSliderInterval: 1,
    };
  },
  created() {
    this.setSliderInterval();
    console.log(this.settingsTemplate);
    this.$emit('settings-changed', { type: 'gradient', settings: this.localSettings.gradient });
    this.$emit('settings-changed', { type: 'layer', settings: this.localSettings.layer });
  },
  methods: {
    getColorGradientCss(gradientName, domain) {
    // Maybe generate an Object when component is created() to prevent render on call.
      const gradientSteps = 30;
      const colorArray = [];
      const step = (this.maxValue - this.minValue) / gradientSteps;
      const colorGradient = chroma
        .scale(gradientName)
        .domain(domain);
      for (let i = 0; i < gradientSteps; i += 1) {
        colorArray.push(colorGradient(this.minValue + (step * i)));
      }
      return `background-image: linear-gradient(to right, ${colorArray})`;
    },
    setSliderInterval() {
      const range = this.minMaxValues[1] - this.minMaxValues[0];
      const orderOfMagnitude = Math.floor(Math.log10(Math.abs(range)));
      this.gradientSliderInterval = 10 ** (orderOfMagnitude - 3);
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
.gradient-overview {
  display: grid !important;
  grid-template-columns: repeat(3, 1fr) !important;
}
.vue-slider {
  border-radius: 1.5rem !important;
  padding: 0px !important;
}
.vue-slider-dot {
  height: 1.5rem !important;
}
.vue-slider-dot-handle {
  border-radius: 0.75rem !important;
}
.vue-slider-process {
  border-radius: 0px !important;
}
.vue-slider-rail, .vue-slider-process {
  background: none;
}
.gradient-slider-parent {
  padding: .25rem 1.5rem 3rem 1.5rem !important;
}
.gradient-value-input>*>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
/* Firefox */
.gradient-value-input>*>input[type=number] {
  -moz-appearance: textfield;
}
.gradient-value-input>.form-control {
  min-width: 55px;
  background-color: #212529;
  color: #fff;
  font-weight: bold;
  box-shadow: 1px 5px 10px 0px #0000003d;
  text-align: center;
  border: 2px solid #000;
}
.gradient-value-input>.form-control:focus {
  background-color: #000;
  color: #fff;
  border: 2px solid #000;
}
.form-control-sm {
  padding: 0.25rem 0.15rem !important;
}
</style>
