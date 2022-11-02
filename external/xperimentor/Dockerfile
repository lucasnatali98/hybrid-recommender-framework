FROM node:alpine

WORKDIR ./src
COPY package.json .

RUN npm install \
    && npm install typescript -g

COPY . .
EXPOSE 5000
RUN ["node", "www.js"]