/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  theme: {
    extend: {
      // backgroundImage: {
      //   'leftlogin': "url('https://leitepeu.com.br/images/article/2021/artigo_leitepeu_18fev21.jpg')",
      //   // 'footer-texture': "url('/img/footer-texture.png')",
      //  }
    },
  },
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  plugins: [ 
  ],
}