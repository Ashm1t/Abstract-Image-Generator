/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true
  },
  basePath: '/Abstract-Image-Generator',
  env: {
    BACKEND_URL: 'https://abstract-image-generator.onrender.com'
  },
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': './src'
    }
    return config
  }
}

module.exports = nextConfig 
