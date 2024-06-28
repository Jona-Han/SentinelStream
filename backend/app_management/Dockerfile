FROM node:22.3-alpine

WORKDIR /alpine

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

ENV NODE_ENV=development

CMD ["node", "app.js"]