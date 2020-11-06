<template>
  <div class="menu" v-if="settings">
    <div
      v-for="settingsMode in settingsTemplate"
      :key="settingsMode.id"
      class="mb-4"
    >
      <b-button
        v-if="settingsMode.id !== 'generalSettings'"
        variant="link"
        class="settings_mode"
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
              v-model="settings[input.propertyType][input.id]"
              :type="input.type"
              :step="input.step"
              :min="input.min"
              :max="input.max"
              :id="input.id"
              :disabled="
                input.valueDependencyId
                  ? !settings[input.propertyType][input.valueDependencyId]
                  : false
              "
            ></b-form-input>
            <b-form-checkbox
              v-else-if="input.type === 'checkbox'"
              v-model="settings[input.propertyType][input.id]"
              :type="input.type"
              :id="input.id"
              :disabled="
                input.valueDependencyId
                  ? !settings[input.propertyType][input.valueDependencyId]
                  : false
              "
            ></b-form-checkbox>
            <b-dropdown
              class="dropdown-gradient"
              variant="link"
              size="sm"
              v-model="settings[input.propertyType][input.id]"
              v-else-if="input.type === 'dropdownGradient'"
              :id="input.id"
              :disabled="
                input.valueDependencyId
                  ? !settings[input.propertyType][input.valueDependencyId]
                  : false
              "
              ><template v-slot:button-content>
                {{ settings[input.propertyType][input.id].label }}
              </template>
              <b-dropdown-item-button v-for="gradient in input.options" :key="gradient.label" @click="settings[input.propertyType][input.id] = gradient">{{gradient.label}}</b-dropdown-item-button>
            </b-dropdown>
          </b-form-group>
        </b-form-group>
      </b-collapse>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    settings: Object,
    settingsTemplate: Object
  },
  watch: {
    'settings.layer': {
      handler: function () {
        console.log('this.settings settingsMenu emit change: ', this.settings)
        this.$emit('settingsChanged', { type: 'layer', settings: this.settings.layer })
      },
      deep: true
    },
    'settings.material': {
      handler: function () {
        this.$emit('settingsChanged', { type: 'material', settings: this.settings.material })
      },
      deep: true
    },
    'settings.lighting': {
      handler: function () {
        this.$emit('settingsChanged', { type: 'lighting', settings: this.settings.lighting })
      },
      deep: true
    }
  },
  created () {
    console.log('this.settings settingsMenu created: ', this.settings)
    this.$emit('settingsChanged', { type: 'layer', settings: this.settings.layer })
  }
}
</script>

<style>
.menu {
  background-color: #fff;
  width: 369px;
  padding: 20px 40px 10px 40px;
  box-shadow: 10px 30px 60px rgba(0, 0, 0, 0.05);
  border-radius: 25px;
  font-family: "Space Grotesk", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
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
.settings_mode {
  color: #2c3e50 !important;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 400;
  text-decoration: none !important;
  font-size: 12px !important;
}
.settings_mode:hover {
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
}
</style>
