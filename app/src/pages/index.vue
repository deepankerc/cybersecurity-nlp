<template>
  <q-page padding>
    <q-search v-model="searchTerm" v-on:input="filter">
      <q-autocomplete
        :static-data="{field: 'value', list: phrases}"
      />
    </q-search>
    <q-infinite-scroll :handler="loadMore">
      <q-card class="q-ma-sm" v-for="(elem, index) in sentences" :key="index">
        <q-card-title>
          {{ elem.country }}
        </q-card-title>
        <q-card-separator />
        <q-card-main>
          {{ elem.text }}
        </q-card-main>
      </q-card>
      <q-spinner-dots slot="message" :size="40"></q-spinner-dots>
    </q-infinite-scroll>
  </q-page>
</template>

<style>
</style>

<script>
import TestData from "assets/test_data.json";
import phrases from "assets/phrases.json";
import * as JsSearch from 'js-search';

const pageSize = 10;

// Setup the search index
var search = new JsSearch.Search('text');
search.addIndex('text');
search.addDocuments(TestData);

// Top phrases for Autocomplete
function parsePhrases() {
  return phrases.map(phrase => {
    return {
      label: phrase,
      value: phrase
    }
  })
}


export default {
  name: 'PageIndex',
  data() {
    return {
      testData: TestData,
      sentences: TestData.slice(0, 10),
      searchTerm: null,
      phrases: parsePhrases()
    }
  },
  methods: {
    loadMore(index, done) {
      let newStart = index * pageSize;
      let newEnd = newStart + pageSize;
      let newSentences = this.testData.slice(newStart, newEnd);
      this.sentences = this.sentences.concat(newSentences);
      done();
    },
    filter(newVal) {
      if (newVal == "") {
        this.testData = TestData;
      }
      else {
        this.testData = search.search(newVal);
      }
      this.sentences = this.testData.slice(0, pageSize);
    }
  }
}
</script>
