
library(ggplot2)

df <- read.csv('pathway_data.csv')

#remove the columns index, column 8 and column 9
df <- df[, -c(1, 8, 9)]

# create barplot where the x-axis is the pathway and the y-axis is the adjusted p-value

pdf("pathway_barplot.pdf", width = 10, height = 10)

ggplot(df, aes(x = reorder(Pathway, -Adjusted.p.value), y = Adjusted.p.value)) +
  geom_bar(stat = "identity", fill = "#01c0b1") +
  coord_flip() +  
  theme_minimal() +  
  geom_text(aes(label = Pathway, y = 0), hjust = -0.1, angle = 0, color = "black") +
  labs(x = "Pathway", y = "Adjusted p-value") +
  theme(axis.text.y = element_blank(), 
        axis.ticks.y = element_blank()) 

dev.off()
