import { FlatCompat } from '@eslint/eslintrc';
import vuePlugin from 'eslint-plugin-vue';

const compat = new FlatCompat({
  baseDirectory: __dirname,
  resolvePluginsRelativeTo: __dirname
});

export default [
  ...compat.config({
    env: { browser: true },
    parserOptions: {
      parser: 'babel-eslint'
    },
    plugins: ['vue'],
    extends: ['plugin:vue/essential', 'standard'],
    rules: {
      'generator-star-spacing': 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off'
    }
  }),
  {
    files: ['src/**/*.{js,vue}'],
    ignores: ['build/**', 'config/**', 'dist/**', '*.js']
  }
];
