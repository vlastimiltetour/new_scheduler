FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

# Vite musí běžet na --host 0.0.0.0, aby byl přístupný zvenčí kontejneru
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]