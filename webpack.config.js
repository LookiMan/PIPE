require('dotenv').config();

const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

const isProduction = process.env.NODE_ENV === 'production';
const jQuery = path.resolve(__dirname, './app/static/assets/vendor/js/jquery-3.6.0.min.js');


const config = {
    entry: './app/static/assets/js/app.js',
    mode: process.env.NODE_ENV,
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'app/static/assets/dist'),
    },
    module: {
        rules: [
            {
                test: /\.(sa|sc|c)ss$/,
                use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader']
            },
        ],
    },
    resolve: {
        alias: {
            'jQuery': jQuery,
            'jquery': jQuery,
            '$': jQuery,
        }
    },
    plugins: [
        new CleanWebpackPlugin(),
        new MiniCssExtractPlugin({
            filename: 'bundle.css'
        })
    ],
};


module.exports = (env, argv) => {
    if (isProduction) {
        config.plugins.push(new UglifyJsPlugin());
        config.module.rules.push({
            test: /\.js$/,
            exclude: /node_modules/,
            use: 'babel-loader'
        })
    }

    return config;
};
