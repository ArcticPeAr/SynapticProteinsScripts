
library(ggplot2)

df <- read.csv('pathway_data.csv')

#remove the columns index, column 8 and column 9
df <- df[, -c(1, 8, 9)]

# create barplot where the x-axis is the pathway and the y-axis is the adjusted p-value
ggplot(df, aes(x = Pathway, y = Adjusted.p.value)) +
    geom_bar(stat = "identity") +
    geom_text(aes(label = round(Adjusted.p.value, 2)), vjust = -0.5) +  # Add text labels inside the bars
    theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
    labs(title = "Pathway Enrichment Analysis", x = "Pathway", y = "Adjusted P-value") +
    theme_minimal() +
    theme(plot.title = element_text(hjust = 0.5))
