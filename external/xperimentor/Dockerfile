FROM node:latest

WORKDIR /src
COPY . .
COPY package.json .
COPY tsconfig.json .


RUN npm install \
    && npm install typescript -g

RUN ls
RUN tsc --build ./tsconfig.json

EXPOSE 3000
CMD ["npm", "start"]