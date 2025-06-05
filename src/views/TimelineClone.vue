<template>
  <BaseView class="container-fluid">
    <template v-slot:main-content>
      <iframe src="/timeline_clone.html" style="width:100%;height:100vh;border:none;"></iframe>
    </template>
  </BaseView>
</template>

<script>
export default {
  name: 'timeline-clone'
};
</script>

<style scoped>
iframe {
  width: 100%;
  height: 100vh;
  border: none;
}
</style>
