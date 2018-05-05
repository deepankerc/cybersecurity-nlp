<template>
  <q-layout view="lHh Lpr lFf">
    <q-layout-header>
      <q-toolbar
        color="light-blue"
        :glossy="$q.theme === 'mat'"
        :inverted="$q.theme === 'ios'"
      >
        <q-btn
          flat
          dense
          round
          @click="leftDrawerOpen = !leftDrawerOpen"
          aria-label="Menu"
        >
          <q-icon name="menu" />
        </q-btn>

        <q-toolbar-title>
          Cybersecurity Strategies Explorer
          <!-- <div slot="subtitle"></div> -->
        </q-toolbar-title>
      </q-toolbar>
    </q-layout-header>

    <q-layout-drawer
      v-model="leftDrawerOpen"
      :content-class="$q.theme === 'mat' ? 'bg-grey-2' : null"
    >
      <q-list
        no-border
        link
        inset-delimiter
      >
        <q-list-header>All Reports</q-list-header>
        <q-item v-for="doc in docData" :key="doc.id" @click.native="openURL(doc.url)">
          <q-item-side icon="place" />
          <q-item-main :label="doc.country" :sublabel="doc.year" />
        </q-item>
      </q-list>
    </q-layout-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { openURL } from 'quasar'
import DocData from "assets/doc_data.json";

DocData.sort(function(a, b) {
  if (a.year === 'Unknown') {
    return 1;
  } else if (b.year === 'Unknown') {
    return -1;
  } else {
    return b.year - a.year;
  }
});

export default {
  name: 'LayoutDefault',
  data () {
    return {
      leftDrawerOpen: this.$q.platform.is.desktop,
      docData: DocData
    }
  },
  methods: {
    openURL
  }
}
</script>

<style>
</style>
