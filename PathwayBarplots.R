
library(ggplot2)

# Read in data fetched from Enrichr with Python script
df <- read.csv('pathway_data.csv')

#remove the columns index, column 8 and column 9
df <- df[, -c(1, 8, 9)]

# remove rows with p-value > 0.01
df <- df[df$Adjusted.p.value < 0.01,]

# add a space to the beginning of each pathway name for pretty bar plot <3
df$Pathway <- paste0(" ", df$Pathway)

# create barplot where the x-axis is the pathway and the y-axis is the adjusted p-value

# Barplot with adjusted p-value
pdf("pathway_barplot_AdjP.pdf", width = 15, height = 10)

ggplot(df, aes(x = reorder(Pathway, -Adjusted.p.value), y = Adjusted.p.value)) +
  geom_bar(stat = "identity", fill = "#01c0b1") +
  coord_flip() +  
  theme_minimal() +  
  geom_text(aes(label = Pathway, y = 0), hjust = 0.0, vjust = 0.8, angle = 0, color = "black", position = position_identity()) +
  labs(x = "Pathway", y = "Adjusted p-value") +
  theme(
    axis.text.y = element_blank(), 
    axis.ticks.y = element_blank(),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank()
  )

dev.off()


# Barplot with Odds Ratio
pdf("pathway_barplot_OR_shortest_at_bottoms.pdf", width = 15, height = 10)

ggplot(df, aes(x = reorder(Pathway, -Odds.Ratio), y = Odds.Ratio)) +
  geom_bar(stat = "identity", fill = "#01c0b1") +
  coord_flip() +  
  theme_minimal() +  
  geom_text(aes(label = Pathway, y = 0), hjust = 0.0, vjust = 0.8, angle = 0, color = "black", position = position_identity()) +
  labs(x = "Pathway", y = "Odds Ratio") +
  theme(
    axis.text.y = element_blank(), 
    axis.ticks.y = element_blank(),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank()
  )

dev.off()

pdf("pathway_barplot_OR_Biggest_at_top.pdf", width = 15, height = 10)

ggplot(df, aes(x = reorder(Pathway, Odds.Ratio), y = Odds.Ratio)) +  # Removed the negative sign for testing
  geom_bar(stat = "identity", fill = "#01c0b1") +
  coord_flip() +  
  theme_minimal() +  
  geom_text(aes(label = Pathway, y = 0), hjust = 0.0, vjust = 0.8, angle = 0, color = "black", position = position_identity()) +
  labs(x = "Pathway", y = "Odds Ratio") +
  theme(
    axis.text.y = element_blank(), 
    axis.ticks.y = element_blank(),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank()
  )

dev.off()
