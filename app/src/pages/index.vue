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
          {{ idToCountry[elem.doc_id] }}
        </q-card-title>
        <q-card-separator />
        <q-card-main>
          {{ elem.text }}
          <a :href=idToURL[elem.doc_id] style="text-decoration: none;"><q-icon name="launch" /></a>
        </q-card-main>
        <q-card-separator />
      </q-card>
      <q-spinner-dots slot="message" :size="40"></q-spinner-dots>
    </q-infinite-scroll>
  </q-page>
</template>

<style>
</style>

<script>
import SentenceData from "assets/sentence_data.json";
import DocData from "assets/doc_data.json";
import phrases from "assets/phrases.json";
import * as JsSearch from 'js-search';

const pageSize = 10;

// Setup the search index
var search = new JsSearch.Search('text');
search.addIndex('text');
search.addDocuments(SentenceData);

// Get URL and country mappings for doc ids
var idToURL = DocData.reduce(function(map, obj) {
    map[obj.id] = obj.url;
    return map;
}, {});
var idToCountry = DocData.reduce(function(map, obj) {
    map[obj.id] = obj.country;
    return map;
}, {});

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
      sentenceData: SentenceData,
      idToCountry: idToCountry,
      idToURL: idToURL,
      sentences: SentenceData.slice(0, 10),
      searchTerm: null,
      phrases: parsePhrases()
    }
  },
  methods: {
    loadMore(index, done) {
      var newStart = index * pageSize;
      var newEnd = newStart + pageSize;
      var newSentences = this.sentenceData.slice(newStart, newEnd);
      this.sentences = this.sentences.concat(newSentences);
      done();
    },
    filter(newVal) {
      if (newVal == "") {
        this.sentenceData = SentenceData;
      }
      else {
        this.sentenceData = search.search(newVal);
      }
      this.sentences = this.sentenceData.slice(0, pageSize);
    }
  }
}
</script>
