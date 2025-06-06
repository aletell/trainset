<template>
  <div class="relative flex size-full min-h-screen flex-col bg-[#111518] overflow-x-hidden" style="font-family: Inter, 'Noto Sans', sans-serif;">
    <div class="layout-container flex h-full grow flex-col">
      <header class="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#283139] px-10 py-3">
        <div class="flex items-center gap-4 text-white">
          <div class="size-4">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" clip-rule="evenodd" d="M24 18.4228L42 11.475V34.3663C42 34.7796 41.7457 35.1504 41.3601 35.2992L24 42V18.4228Z" fill="currentColor" />
              <path fill-rule="evenodd" clip-rule="evenodd" d="M24 8.18819L33.4123 11.574L24 15.2071L14.5877 11.574L24 8.18819ZM9 15.8487L21 20.4805V37.6263L9 32.9945V15.8487ZM27 37.6263V20.4805L39 15.8487V32.9945L27 37.6263ZM25.354 2.29885C24.4788 1.98402 23.5212 1.98402 22.646 2.29885L4.98454 8.65208C3.7939 9.08038 3 10.2097 3 11.475V34.3663C3 36.0196 4.01719 37.5026 5.55962 38.098L22.9197 44.7987C23.6149 45.0671 24.3851 45.0671 25.0803 44.7987L42.4404 38.098C43.9828 37.5026 45 36.0196 45 34.3663V11.475C45 10.2097 44.2061 9.08038 43.0155 8.65208L25.354 2.29885Z" fill="currentColor" />
            </svg>
          </div>
          <h2 class="text-white text-lg font-bold leading-tight tracking-[-0.015em]">DataLabeler</h2>
        </div>
        <div class="flex flex-1 justify-end gap-8">
          <div class="flex items-center gap-9">
            <router-link class="text-white text-sm font-medium leading-normal" :to="{name:'home'}">Overview</router-link>
            <router-link class="text-white text-sm font-medium leading-normal" :to="{name:'timeline'}">Features</router-link>
            <router-link class="text-white text-sm font-medium leading-normal" :to="{name:'help'}">Help</router-link>
            <router-link class="text-white text-sm font-medium leading-normal" :to="{name:'license'}">License</router-link>
            <router-link class="text-white text-sm font-medium leading-normal" :to="{name:'analytics'}">Analytics</router-link>
          </div>
          <button class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-10 px-4 bg-[#0b80ee] text-white text-sm font-bold leading-normal tracking-[0.015em]" @click="upload">
            <span class="truncate">Upload Data</span>
          </button>
        </div>
      </header>
      <div class="px-40 flex flex-1 justify-center py-5">
        <div class="layout-content-container flex flex-col max-w-[960px] flex-1">
          <div class="@container">
            <div class="@[480px]:p-4">
              <div class="flex min-h-[480px] flex-col gap-6 bg-cover bg-center bg-no-repeat @[480px]:gap-8 @[480px]:rounded-xl items-center justify-center p-4" style="background-image: linear-gradient(rgba(0, 0, 0, 0.1) 0%, rgba(0, 0, 0, 0.4) 100%), url('https://lh3.googleusercontent.com/aida-public/AB6AXuCsCy-C7yr2kEW5qK3QCvkZvd9sWiUVEBeTKnDyKGy_GQqy3lVpI2qRu5w-bMAoFM3GNhzt4_CEppUEcJqLBiMwuNU-3eZue-mrkkvtRe-PvZths1mFOrlA4MwEQLNXf3oNYIgNEinBWB7TDzkAa2ayNITonTs0vbrVX3jolZqmM7Sq2qECvfqE6-DhYp2eMxI-KC3RcMcgWUCjK_heMBpn8yQ3wcWpjwZTyK2XHDQOnKuCNEThnifkZIo9QAWMaEzz8LF2-40yuF8');">
                <div class="flex flex-col gap-2 text-center">
                  <h1 class="text-white text-4xl font-black leading-tight tracking-[-0.033em] @[480px]:text-5xl @[480px]:font-black @[480px]:leading-tight @[480px]:tracking-[-0.033em]">Label Time Series Data with Precision</h1>
                  <h2 class="text-white text-sm font-normal leading-normal @[480px]:text-base">Our platform offers a streamlined solution for labeling time series data, enabling you to enhance model accuracy and gain deeper insights. Upload your data and begin labeling with ease.</h2>
                </div>
                <button class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-10 px-4 @[480px]:h-12 @[480px]:px-5 bg-[#0b80ee] text-white text-sm font-bold leading-normal tracking-[0.015em] @[480px]:text-base" @click="upload">
                  <span class="truncate">Upload Data</span>
                </button>
              </div>
            </div>
          </div>
          <input type="file" id="upload-file" ref="fileInput" class="hidden" @change="fileCheck" />
          <div class="flex flex-col gap-10 px-4 py-10 @container">
            <div class="flex flex-col gap-4">
              <h1 class="text-white tracking-light text-[32px] font-bold leading-tight @[480px]:text-4xl @[480px]:font-black @[480px]:leading-tight @[480px]:tracking-[-0.033em] max-w-[720px]">Key Features</h1>
              <p class="text-white text-base font-normal leading-normal max-w-[720px]">Explore the capabilities of our time series data labeling tool.</p>
            </div>
            <div class="grid grid-cols-[repeat(auto-fit,minmax(158px,1fr))] gap-3 p-0">
              <div class="flex flex-1 gap-3 rounded-lg border border-[#3b4854] bg-[#1b2127] p-4 flex-col">
                <div class="text-white" data-icon="File" data-size="24px" data-weight="regular">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256"><path d="M213.66,82.34l-56-56A8,8,0,0,0,152,24H56A16,16,0,0,0,40,40V216a16,16,0,0,0,16,16H200a16,16,0,0,0,16-16V88A8,8,0,0,0,213.66,82.34ZM160,51.31,188.69,80H160ZM200,216H56V40h88V88a8,8,0,0,0,8,8h48V216Z"></path></svg>
                </div>
                <div class="flex flex-col gap-1">
                  <h2 class="text-white text-base font-bold leading-tight">Easy Data Upload</h2>
                  <p class="text-[#9cabba] text-sm font-normal leading-normal">Seamlessly upload your time series data in various formats, including CSV and JSON.</p>
                </div>
              </div>
              <div class="flex flex-1 gap-3 rounded-lg border border-[#3b4854] bg-[#1b2127] p-4 flex-col">
                <div class="text-white" data-icon="Clock" data-size="24px" data-weight="regular">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm64-88a8,8,0,0,1-8,8H128a8,8,0,0,1-8-8V72a8,8,0,0,1,16,0v48h48A8,8,0,0,1,192,128Z"></path></svg>
                </div>
                <div class="flex flex-col gap-1">
                  <h2 class="text-white text-base font-bold leading-tight">Efficient Labeling</h2>
                  <p class="text-[#9cabba] text-sm font-normal leading-normal">Label data points with precision using our intuitive interface, designed for speed and accuracy.</p>
                </div>
              </div>
              <div class="flex flex-1 gap-3 rounded-lg border border-[#3b4854] bg-[#1b2127] p-4 flex-col">
                <div class="text-white" data-icon="ChartLine" data-size="24px" data-weight="regular">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256"><path d="M232,208a8,8,0,0,1-8,8H32a8,8,0,0,1-8-8V48a8,8,0,0,1,16,0v94.37L90.73,98a8,8,0,0,1,10.07-.38l58.81,44.11L218.73,90a8,8,0,1,1,10.54,12l-64,56a8,8,0,0,1-10.07.38L96.39,114.29,40,163.63V200H224A8,8,0,0,1,232,208Z"></path></svg>
                </div>
                <div class="flex flex-col gap-1">
                  <h2 class="text-white text-base font-bold leading-tight">Advanced Analytics</h2>
                  <p class="text-[#9cabba] text-sm font-normal leading-normal">Gain insights into your labeled data with built-in analytics and visualization tools. <router-link class="underline" :to="{name:'analytics'}">Click here</router-link> to see an example page.</p>
                  <p class="text-[#9cabba] text-sm italic">Not yet implemented.</p>
                </div>
              </div>
              <div class="flex flex-1 gap-3 rounded-lg border border-[#3b4854] bg-[#1b2127] p-4 flex-col">
                <div class="text-white" data-icon="Folders" data-size="24px" data-weight="regular">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256"><path d="M224,72H130.67L104,45.33A8,8,0,0,0,98.34,43H32A16,16,0,0,0,16,59V192a16,16,0,0,0,16,16H224a16,16,0,0,0,16-16V88A16,16,0,0,0,224,72ZM32,59H93.33l16,16H224V88H32Z"></path></svg>
                </div>
                <div class="flex flex-col gap-1">
                  <h2 class="text-white text-base font-bold leading-tight">Project Management</h2>
                  <p class="text-[#9cabba] text-sm font-normal leading-normal">Manage multiple datasets and labeling projects. <router-link class="underline" :to="{name:'project-management'}">Click here</router-link> for an example page.</p>
                  <p class="text-[#9cabba] text-sm italic">Not yet implemented.</p>
                </div>
              </div>
              <div class="flex flex-1 gap-3 rounded-lg border border-[#3b4854] bg-[#1b2127] p-4 flex-col">
                <div class="text-white" data-icon="ScatterPlot" data-size="24px" data-weight="regular">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256"><path d="M36,200a12,12,0,1,1,12-12A12,12,0,0,1,36,200Zm184-96a12,12,0,1,0-12-12A12,12,0,0,0,220,104ZM92,84a12,12,0,1,0-12-12A12,12,0,0,0,92,84Zm88,120a12,12,0,1,0,12,12A12,12,0,0,0,180,204Zm-56-52a12,12,0,1,0-12-12A12,12,0,0,0,124,152Z"></path></svg>
                </div>
                <div class="flex flex-col gap-1">
                  <h2 class="text-white text-base font-bold leading-tight">Data Exploration</h2>
                  <p class="text-[#9cabba] text-sm font-normal leading-normal">Discover relationships with scatter plots and correlation tools. <router-link class="underline" :to="{name:'explore'}">Click here</router-link> for an example page.</p>
                  <p class="text-[#9cabba] text-sm italic">Not yet implemented.</p>
                </div>
              </div>
            </div>
          </div>
          <p class="text-[#9cabba] text-base font-normal leading-normal text-center mt-6">This project is a fork of <a href="https://github.com/Geocene/trainset" class="underline" target="_blank">TRAINSET</a>.</p>
        </div>
      </div>
    </div>
    <div v-if="loading" class="absolute inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="h-12 w-12 animate-spin rounded-full border-4 border-white border-t-transparent"></div>
    </div>
  </div>
</template>

<script>
const { DateTime } = require('luxon');

export default {
  name: 'index',
  data () {
    return {
      errorUpload: false,
      loading: false
    };
  },
  props: {
    nextUp: Boolean
  },
  methods: {
    error (msg) {
      this.errorUpload = true;
      this.$router.push({
        name: 'labeler',
        params: {
          csvData: [],
          minMax: [],
          filename: '',
          headerStr: '',
          isValid: false,
          failMessage: msg
        }
      });
    },
    shouldUpload () {
      if (this.nextUp === true) {
        setTimeout(() => this.upload(), 100);
      }
    },
    upload () {
      this.$refs.fileInput.click();
    },
    fileCheck () {
      this.loading = true;
      const fileInput = document.getElementById('upload-file').files.item(0);
      const filename = fileInput.name;
      const baseName = filename.replace(/\.[^/.]+$/, '');
      const reader = new FileReader();
      const seriesList = new Set();
      const labelList = new Set();
      const plotDict = [];
      let headerStr;

      reader.readAsText(fileInput);
      reader.onloadend = () => {
        headerStr = reader.result.split(/\r?\n/)[0];
        const parseCsv = require('@/utils/parseCsv');
        let parsed;
        try {
          parsed = parseCsv(reader.result, filename);
        } catch (e) {
          this.error(e.message);
          return;
        }
        parsed.forEach((row, idx) => {
          const date = DateTime.fromJSDate(row.timestamp);
          seriesList.add(row.series);
          if (row.label) labelList.add(row.label);
          plotDict.push({
            id: idx.toString(),
            val: row.value.toString(),
            time: date,
            series: row.series,
            label: row.label
          });
        });
        if (!this.errorUpload) {
          this.$router.push({
            name: 'labeler',
            params: {
              csvData: plotDict,
              filename: baseName,
              headerStr: headerStr,
              seriesList: Array.from(seriesList),
              labelList: Array.from(labelList),
              isValid: true
            }
          });
        }
        this.loading = false;
      };
    }
  },
  created () {
    this.shouldUpload();
  }
};
</script>

<style scoped>
</style>
