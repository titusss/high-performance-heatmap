<template>
  <div class="menu">
    <div
      v-for="settingsMode in settingsTemplate"
      :key="settingsMode.id"
      class="mb-3"
    >
      <b-button
        variant="link"
        class="settings_mode"
        v-b-toggle="settingsMode.id"
        size="sm"
        >{{ settingsMode.label }}</b-button
      >
      <b-collapse
        :id="settingsMode.id"
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
              :v-model="input.value"
              :type="input.type"
              :step="input.step"
              :min="input.min"
              :max="input.max"
              :id="input.id"
            ></b-form-input>
            <b-form-checkbox
              v-else-if="input.type === 'checkbox'"
              :v-model="input.value"
              :type="input.type"
              :id="input.id"
            ></b-form-checkbox>
          </b-form-group>
        </b-form-group>
      </b-collapse>
    </div>
  </div>
</template>

<script>
import settingsTemplate from '@/assets/settingsTemplate.json'
export default {
  data () {
    return {
      settingsTemplate
    }
  }
}
</script>

<style>
.menu {
  background-color: #fff;
  width: 369px;
  padding: 40px;
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
</style>
