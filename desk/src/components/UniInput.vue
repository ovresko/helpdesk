<template>
  <div class="space-y-1.5">
    <span class="block text-sm text-gray-700">
      {{ field.label }}
      <span v-if="field.required" class="place-self-center text-red-500">
        *
      </span>
      <button v-if="transValue" @click="clearSelection" class="ml-2 text-red-500">
        Effacer
      </button>

    </span>
    <component
      :is="component"
      :placeholder="placeholder"
      :value="transValue"
      :model-value="transValue"
      @update:model-value="emitUpdate(field.fieldname, $event)"
      @change="emitUpdate(field.fieldname, $event.value || $event)"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, h } from "vue";
import { createResource, Autocomplete, FormControl } from "frappe-ui";
import { Field } from "@/types";
import SearchComplete from "./SearchComplete.vue";
import { onMounted, watch, ref, isProxy, toRaw, reactive } from "vue";
import { emitter } from "@/emitter";

type Value = string | number | boolean;

interface P {
  field: Field;
  value: Value;
}

interface R {
  fieldname: Field["fieldname"];
  value: Value;
}

interface E {
  (event: "change", value: R);
}

const props = defineProps<P>();
const emit = defineEmits<E>();
const shouldRecompute = ref(false);

const component = computed(() => {
  if (shouldRecompute.value) {
    return null;
  }

  if (props.field.url_method) {
    return h(Autocomplete, {
      options: apiOptions.data,
    });
  } else if (props.field.fieldtype === "Link" && props.field.options) {
    return h(SearchComplete, {
      doctype: props.field.options,
    });
  } else if (props.field.fieldtype === "Select") {
    return h(Autocomplete, {
      options: props.field.options
        .split("\n")
        .map((o) => ({ label: o, value: o })),
    });
  } else if (props.field.fieldtype === "Check") {
    return h(Autocomplete, {
      options: [
        {
          label: "Yes",
          value: 1,
        },
        {
          label: "No",
          value: 0,
        },
      ],
    });
  } else {
    return h(FormControl, {
      debounce: 500,
    });
  }
});

const apiOptions = createResource({
  url: props.field.url_method,
  auto: !!props.field.url_method,
  transform: (data) =>
    data.map((o) => ({
      label: o,
      value: o,
    })),
});

const transValue = computed(() => {
  if (props.field.fieldtype === "Check") {
    return props.value ? "Yes" : "No";
  }
  return props.value;
});

const placeholder = computed(() => {
  if (props.field.fieldtype === "Data" && !props.field.url_method) {
    return "Type something";
  }
  return "Select an option";
});

function emitUpdate(fieldname: Field["fieldname"], value: Value) {
  emit("change", { fieldname, value });
  emitter.emit("fchange", { fieldname, value });
}

onMounted(() => {
  emitter.on("fchange", function (e: any) {
    if (
      ["custom_type", "custom_agent"].includes(props.field.fieldname) &&
      e.fieldname == "custom_team"
    ) {
      var iwant = "types";
      if (props.field.fieldname == "custom_agent") {
        iwant = "agents";
      }
      let todos = createResource({
        url: "helpdesk.extends.client.get_types", // [!code --]
        params: {
          iwant: iwant,
          team: e.value,
        }, // iwant=None,resource=None,team=None
      });
      var res = todos.fetch();
      res.then((response) => {
        console.log("response", response);
        if (isProxy(response)) {
          response = toRaw(response);
        }
        apiOptions.data = response.types.map((o) => ({
          label: o,
          value: o,
        }));
        shouldRecompute.value = true;
        console.log("data", apiOptions.data);
        shouldRecompute.value = false;
      });
    }
  });
});

function clearSelection() {
  emitUpdate(props.field.fieldname, null); // Set the value to null to clear the selection
}

</script>
