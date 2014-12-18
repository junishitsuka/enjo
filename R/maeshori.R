train <- read.csv('~/Desktop/lab/炎上分析/data/output/train/train_10/train_10.csv')

# 欠損値の処理
train <- na.omit(train)
# train$Cluster <- ifelse(is.na(train$Cluster), mean(train$Cluster, na.rm=TRUE), train$Cluster)
# train$Degree <- ifelse(is.na(train$Degree), mean(train$Degree, na.rm=TRUE), train$Degree)

plus <- subset(train, Burst == 1)
minus <- subset(train, Burst == 0)
minus <- minus[sample(nrow(plus)),]
train <- rbind(plus, minus)

# Randomly shuffle the data
data<-train[sample(nrow(train)),]

write.csv(data, '~/Desktop/lab/炎上分析/data/output/train/train_10/train_10_naomit_sampled.csv', row.names = FALSE)
