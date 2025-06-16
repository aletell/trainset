<template>
  <div class="relative flex min-h-screen flex-col bg-[#111518] overflow-x-hidden" style="font-family: Inter, 'Noto Sans', sans-serif;">
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
        </div>
      </header>
      <div class="px-40 flex flex-1 justify-center py-5">
        <div class="layout-content-container flex flex-col max-w-[960px] flex-1">
          <div class="flex flex-col gap-6 px-4 py-10 text-white">
            <h1 class="text-2xl font-bold">Advanced Analytics</h1>
            <p class="text-[#9cabba] text-base">Gain insights into your labeled data with built-in analytics and visualization tools.</p>
            <p class="text-[#9cabba] text-base italic">Not yet implemented.</p>
          </div>
          <p class="text-[#9cabba] text-base font-normal leading-normal text-center mt-6">This project is a fork of <a href="https://github.com/Geocene/trainset" class="underline" target="_blank">TRAINSET</a>.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default { name: 'analytics' };
</script>

<style scoped>
</style>
