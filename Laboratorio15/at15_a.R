#Nome: Elizabeth Borgognoni Souto
#Aplicativo 1

#instalando os pacotes 
#pkgs <- c('MASS', 'tidyverse', 'magrittr', 'RSQLite', 'shiny')
#install.packages(pkgs)

#carregando os pacotes
library(MASS)
library(tidyverse)
library(magrittr)
library(RSQLite)
library(shiny)

ui <- fluidPage(
    
    #Titulo
    titlePanel("Analise dos dados DDT"),
    
    sidebarLayout(
        sidebarPanel( # Página lateral, com interação
            sliderInput(inputId = "caixas",# Input: Slider com o número de caixas
                label = "Numero de caixas:",
                min = 4,
                max = 10,
                value = 14),
            checkboxGroupInput("checkbox", choices = list("Media" = mean(DDT),"Mediana"= median(DDT),
                "Desvio padrão" = sd(DDT),"IQR" = IQR(DDT)/1.35), 
                label = h3("Análises estatísticas"), selected = mean(DDT)),
            fluidRow(column(8, verbatimTextOutput("value")))
        ),
        
        # Conteúdo da página principal, no nosso caso mostra um gráfico
        mainPanel(
            plotOutput("Histograma") # Etiqueta no output
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output){
    
    output$Histograma <- renderPlot({ # Coloca resultados no output
        # Extrai caixas do input
        hist(DDT, breaks = input$caixas, col = 'blue', border = 'white', 
            main = "Histograma de DDT", xlab = "Valores de DDT", ylab = "Frequencia", freq = FALSE)
        f1 <- function(x) dnorm(x, mean = mean(DDT), sd = sd(DDT))
        curve(f1, add = TRUE, col = "Purple")
        f2 <- function(x) dnorm(x, mean = median(DDT), sd = IQR(DDT)/1.35)
        curve(f2, add = TRUE, col = "Red")
        legend("topright", legend = c("Curva f1", "Curva f2"), lty=c(1,1), lwd=c(2.5,2.5),col=c("purple","red"))
    })
    output$value <- renderPrint({ input$checkbox })
    
    
    
    
}

shinyApp(ui = ui, server = server)
