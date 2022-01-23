# pull official base image
FROM node:13.12.0-alpine

# set working directory
WORKDIR /aiobankingui/app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /aiobankingui/app/node_modules/.bin:$PATH

# install app dependencies
COPY /aiobankingui/package.json ./
COPY /aiobankingui/package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent

# add app
COPY ./aiobankingui .

# start app
CMD ["npm", "start"]