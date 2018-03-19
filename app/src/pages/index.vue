<template>
  <div>
    <q-search v-model="searchTerm" v-on:input="filter" />
    <q-infinite-scroll :handler="loadMore">
      <q-card v-for="(elem, index) in sentences" :key="index">
        <q-card-title>
          {{ elem.country }}
        </q-card-title>
        <q-card-separator />
        <q-card-main>
          {{ elem.text }}
        </q-card-main>
      </q-card>
      <!--
        slot="message" for DOM element to display (in this example
        a dots spinner) when loading additional content
      -->
      <q-spinner-dots slot="message" :size="40"></q-spinner-dots>
    </q-infinite-scroll>
  </div>
</template>

<style>
</style>

<script>
import TestData from "../assets/test_data.json";
import * as JsSearch from 'js-search';

const pageSize = 10;

// Setup the search index
var search = new JsSearch.Search('text');
search.addIndex('text');
search.addDocuments(TestData);

export default {
  name: 'PageIndex',
  data() {
    return {
      testData: TestData,
      sentences: TestData.slice(0, 10),
      searchTerm: null
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
