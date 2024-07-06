FROM node:22.3-alpine

WORKDIR /data_ingestion

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 4001

ENV NODE_ENV=development

CMD ["node", "app.js"]