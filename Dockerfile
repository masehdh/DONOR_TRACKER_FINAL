FROM nikolaik/python-nodejs:python3.8-nodejs12-alpine

WORKDIR /usr/src/app

COPY package*.json ./

COPY requirements.txt ./

RUN npm install && pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["npm", "start"]