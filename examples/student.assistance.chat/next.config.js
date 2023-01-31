/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    loader: 'akamai',
    path: 'https://noop/',
  },
}

module.exports = nextConfig
