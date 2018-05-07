<template>
  <q-page padding>
    <div>
      <q-search v-model="searchTerm" v-on:input="filterOnSearch" placeholder="Search for a topic or keyphrase">
        <q-autocomplete
          :static-data="{field: 'value', list: phrases}"
        />
      </q-search>
    </div>
    <div>
      <q-select
        multiple
        float-label="Select Countries"
        v-model="selectedCountries"
        :options="countryOptions"
        :filter=true
        @input="filterOnCountrySelect"
      />
    </div>
    <q-modal v-model="modalOpen" :content-css="{minWidth: '60vw', minHeight: '80vh'}">
      <q-modal-layout>
        <q-toolbar slot="header">
          <q-toolbar-title v-if="modalElem !== null">
            {{ idToCountry[modalElem.doc_id] }} ({{ idToYear[modalElem.doc_id] }}) <a :href="idToURL[modalElem.doc_id]" target="_blank" style="text-decoration: none;"><q-icon name="launch" /></a>
          </q-toolbar-title>
        </q-toolbar>

        <q-toolbar slot="footer">
          <q-btn
            color="primary"
            v-close-overlay
            label="Close"
            class="absolute-right"
          />
        </q-toolbar>

        <div class="layout-padding">
          <span v-html="modalText"></span>
        </div>
      </q-modal-layout>
    </q-modal>
    <q-infinite-scroll :handler="loadMore">
      <q-card class="q-ma-sm" v-for="(elem, index) in sentences" :key="index">
        <q-card-title>
          {{ idToCountry[elem.doc_id] }} ({{ idToYear[elem.doc_id] }})
        </q-card-title>
        <q-card-separator />
        <q-card-main>
          {{ elem.text }} <q-icon name="launch" @click.native="openModal(elem)" />
        </q-card-main>
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
var idToYear = DocData.reduce(function(map, obj) {
  map[obj.id] = obj.year;
  return map;
}, {});

// Get unique countries
function uniqueCountries(d) {
  var uniq = d.reduce(function(map, obj) {
    map[obj.country] = true;
    return map;
  }, {});
  uniq = Object.keys(uniq);
  uniq.sort();
  return uniq.map(function(x) {
    return {
      label: x,
      value: x
    };
  });
}

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
      idToYear: idToYear,
      sentences: SentenceData.slice(0, 10),
      searchTerm: null,
      phrases: parsePhrases(),
      modalText: null,
      modalElem: null,
      modalOpen: false,
      countryOptions: uniqueCountries(DocData),
      selectedCountries: [],
    }
  },
  methods: {
    loadMore(index, done) {
      var newStart = this.sentences.length;
      var newEnd = newStart + pageSize;
      var newSentences = this.sentenceData.slice(newStart, newEnd);
      this.sentences = this.sentences.concat(newSentences);
      done();
    },
    filterOnSearch(newVal) {
      if (newVal == "") {
        this.sentenceData = SentenceData;
      }
      else {
        this.sentenceData = search.search(newVal);
      }
      if (this.selectedCountries.length > 0) {
        this.sentenceData = this.sentenceData.filter(
        sentence => this.selectedCountries.includes(this.idToCountry[sentence.doc_id]));
      }
      this.sentences = this.sentenceData.slice(0, pageSize);
    },
    filterOnCountrySelect(newVal) {
      this.filterOnSearch(this.searchTerm == null ? '' : this.searchTerm);
    },
    openModal(elem) {
      var modalSentences = SentenceData.filter(
        x => x.paragraph_id === elem.paragraph_id).sort(
          function(a, b) {
            return a.id.split('_')[1] - b.id.split('_')[1];
          }
        );
      var modalSentencesText = Array(modalSentences.length);
      for (var i = 0; i < modalSentences.length; i++) {
        modalSentencesText[i] = '';
        
        // Add indent for lists
        if (modalSentences[i].indent && i != 0) {
          modalSentencesText[i] += '<br><br>';
        }

        // Bold the original clicked sentence
        if (modalSentences[i].id == elem.id) {
          modalSentencesText[i] += '<strong>' + modalSentences[i].text + '</strong>';
        } else {
          modalSentencesText[i] += modalSentences[i].text;
        }

      }
      this.modalText = '<p>' + modalSentencesText.join(' ') + '</p>';
      this.modalElem = elem;
      this.modalOpen = true;
    }
  }
}
</script>
