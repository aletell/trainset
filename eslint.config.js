import js from '@eslint/js';
import vue from 'eslint-plugin-vue';
import vueParser from 'vue-eslint-parser';

export default [
  js.configs.recommended,
  {
    files: ['src/**/*.{js,vue}'],
    ignores: ['build/**', 'config/**', 'dist/**'],
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
      'no-self-assign': 'off'
    }
  }
];
