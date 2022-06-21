FROM node:12.18.1
WORKDIR /app
COPY ./frontend/app /app
RUN npm install
EXPOSE 4000
CMD ["npm", "run", "dev"]