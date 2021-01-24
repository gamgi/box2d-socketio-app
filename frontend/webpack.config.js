const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin')
const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
  mode: 'production',
  entry:  {
    main: './src/index.ts'
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.(png|jpg|svg)$/i,
        use: 'file-loader',
        include: [path.resolve(__dirname, 'src/assets')],
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'build'),
  },
  plugins: [
    new HtmlWebpackPlugin({
      template:'./src/index.html',
      minify: false
    }),
    new CopyPlugin({
      patterns: [
        { from: './src/style.css', to: 'style.css'},
        { from: './src/assets', to: 'assets/'},
      ]
    })
  ]
};