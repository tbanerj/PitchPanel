import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte(), tailwindcss()],
  server: {
    port: 3000,
    proxy: {
      "/api": "http://localhost:5000", // reroutes all api requests to port 8000 on host (fastapi server)
    }
  }
})
