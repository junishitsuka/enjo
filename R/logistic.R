library(randomForest)
library(e1071)

# データフレームを一括スケーリングする関数
scale_matrix <- function(x) {
    x_scaled <- x
    for (i in 1:ncol(x)) {
        x_scaled[i] <- scale(x[,i])
    }
    return(x_scaled)
}

logistic <- function(trainData, testData) {
    # train.logistic <- glm(Burst ~ Hashtag + Mention + URL + Length + Reply + Follower + Follow + Favorite + Entry, data = trainData, family = binomial(link = "logit"))
    train.logistic <- glm(Burst~., data = trainData, family = binomial(link = "logit"))
    # print(summary(train.logistic))
    pred <- round(predict(train.logistic, testData, type = "response"))
    return(pred)
}

rf <- function(trainData, testData) {
    # train.rf <- randomForest(Burst ~ Hashtag + Mention + URL + Length + Reply + Follower + Follow + Favorite + Entry, data = trainData)
    train.rf <- randomForest(Burst~., data = trainData)
    # print(tuneRF(trainData[,-1], trainData[,1],doBest=T))
    # print(importance(train.rf))
    pred <- predict(train.rf, testData, type = "response")
    return(pred)
}

libsvm <- function(trainData, testData) {
    # train.svm <- svm(Burst ~ Hashtag + Mention + URL + Length + Reply + Follower + Follow + Favorite + Entry, data = trainData, gamma = 0.05882353, cost = 1.0, kernel = "radial")
    train.svm <- svm(Burst ~ Mention + URL + Length + Follower + Follow + Favorite + Entry + Degree + Pagerank, data = trainData, gamma = 0.05882353, cost = 1.0, kernel = "radial")
    # train.svm <- svm(Burst~., data = trainData, gamma = 0.05882353, cost = 1.0, kernel = "radial")
    # t = tune.svm(Burst~., data = trainData)
    # print(t$best.model)
    pred <- predict(train.svm, testData, type = "response")
    return(pred)
}

Accuracy <- 0
Precision <- 0
Recall <- 0
Fvalue <- 0

train <- read.csv('~/Desktop/lab/炎上分析/data/output/train.csv')

# 欠損値の処理
train <- na.omit(train)
# train$Cluster <- ifelse(is.na(train$Cluster), mean(train$Cluster, na.rm=TRUE), train$Cluster)
# train$Degree <- ifelse(is.na(train$Degree), mean(train$Degree, na.rm=TRUE), train$Degree)

# scaling
train <- train[,-c(11)]
train.scaled <- scale_matrix(train)
train.scaled[,1] <- as.factor(train[,1])
train <- train.scaled

plus <- subset(train, Burst == 1)
minus <- subset(train, Burst == 0)
minus <- minus[sample(nrow(plus)),]
train <- rbind(plus, minus)

# Randomly shuffle the data
data<-train[sample(nrow(train)),]

# Create 10 equally size folds
folds <- cut(seq(1, nrow(data)), breaks = 10, labels = FALSE)

#Perform 10 fold cross validation
for(i in 1:10){
     #Segement your data by fold using the which() function
     testIndexes <- which(folds==i,arr.ind=TRUE)
     testData <- data[testIndexes, ]
     trainData <- data[-testIndexes, ]

     pred <- libsvm(trainData, testData)
     t <- table(pred, testData[,1])
     accuracy <- (t[1] + t[4]) / sum(t)
     precision <- t[4] / (t[2] + t[4])
     recall <- t[4] / (t[4] + t[3])
     f <- 2 * precision * recall / (precision + recall)

     Accuracy <- Accuracy + accuracy
     Precision <- Precision + precision
     Recall <- Recall + recall
     Fvalue <- Fvalue + f
}

print(Accuracy / 10)
print(Precision / 10)
print(Recall / 10)
print(Fvalue / 10)
