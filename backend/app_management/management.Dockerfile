FROM node:22.3-alpine

WORKDIR /app_management

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 4000

ENV NODE_ENV=development

CMD ["node", "app.js"]