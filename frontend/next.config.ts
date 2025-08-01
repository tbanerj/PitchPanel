import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async headers() {
    return [
      {
        // Apply these headers to all routes
        source: "/(.*)",
        headers: [
          {
            key: "Access-Control-Allow-Origin",
            value: "*", // Or specify your Uvicorn server URL like "http://localhost:8000"
          },
          {
            key: "Access-Control-Allow-Methods",
            value: "GET, POST, PUT, DELETE, OPTIONS",
          },
          {
            key: "Access-Control-Allow-Headers",
            value: "Content-Type, Authorization",
          },
          {
            key: "Access-Control-Allow-Credentials",
            value: "true",
          },
        ],
      },
    ];
  },
  images: {
    domains: [
      "singersroom.com",
      "antares-wp-media.sfo2.digitaloceanspaces.com",
      "png.pngtree.com",
      "https://stock.adobe.com",
      "t4.ftcdn.net",
      "miro.medium.com"
    ]
  }

  // Other Next.js config options can go here
};

export default nextConfig;
