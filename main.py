from website import create_app
# This is a test comment to check Git changes

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


# button {
#     font -family: inherit;
#     font -size: 20px;
#     background: royalblue;
#     color: white;
#     padding -left: 0.9em ;
#     display: flex;
#     align -items: center;
#     border: none;
#     border -radius: 16px;
#     overflow: hidden;
#     transition: all 0.2s;

# }

# button span{
#     display: block;
#     margin -left: 0.3em;
#     transition: all 0.3s;
#     ease-in-out;

# }

# button svg{
#     display: block;
#     transform-origin: center center;
#     transition: transform 0.3s ease-in-out;
# }

# akeyframes fly-1{
#     from{
#         transform: translateY(0.1em);
#     }
#     to{
#         transform: translateY(-0.1em);
#     }
# }