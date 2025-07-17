import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	build: {
		outDir: './build',
	},
	server: {
		port: 3000,
		proxy: {
			"/api": "http://localhost:8000"
		}
	}
});
