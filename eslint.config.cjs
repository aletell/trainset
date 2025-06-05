const js = require('@eslint/js');
const vue = require('eslint-plugin-vue');
const vueParser = require('vue-eslint-parser');

module.exports = [
  js.configs.recommended,
  {
    files: ['src/**/*.{js,vue}'],
    ignores: ['build/**', 'config/**', 'dist/**', '/*.js'],
    languageOptions: {
      parser: vueParser,
      parserOptions: {
        parser: 'babel-eslint',
        ecmaVersion: 2020,
        sourceType: 'module'
      },
      globals: {
        $: 'readonly',
        jQuery: 'readonly'
      }
    },
    plugins: { vue },
    rules: {
      'no-debugger': 'off',
      'no-undef': 'off',
      'no-unused-vars': 'off',
      'no-cond-assign': 'off',
      'no-extra-boolean-cast': 'off',
      'no-empty': 'off',
      'no-self-assign': 'off',
      'no-extra-semi': 'off',
      'no-mixed-spaces-and-tabs': 'off'
    }
  }
];
