Accuracy <- 0
Precision <- 0
Recall <- 0
Fvalue <- 0

train <- read.csv('~/Desktop/lab/炎上分析/data/output/train_community.csv')
na.omit(train)
# train$Cluster <- ifelse(is.na(train$Cluster), mean(train$Cluster, na.rm=TRUE), train$Cluster)
# train$Degree <- ifelse(is.na(train$Degree), mean(train$Degree, na.rm=TRUE), train$Degree)

plus <- subset(train, Burst == 1)
minus <- subset(train, Burst == 0)
minus <- minus[sample(nrow(plus)),]
train <- rbind(plus, minus)

write.csv(train, '../../data/output/data.csv')

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

     train.logistic <- glm(Burst ~ Hashtag + Mention + URL + Length + Reply + Follower + Follow + Favorite + Entry, data = trainData, family = binomial(link = "logit"))
     pred <- round(predict(train.logistic, testData, type = "response"))
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
