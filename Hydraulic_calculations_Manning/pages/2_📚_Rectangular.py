import streamlit as st
import os
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from streamlit_extras.stylable_container import stylable_container
from Report.report import Report
from Report.Utils import Utils
from datetime import datetime


#### Functions
def estimate_rectang_y(B, h, Q, s, n):
    y = sp.symbols('y')
    f_Q = ((B * y) / (B + 2 * y))**(2 / 3) * sp.sqrt(s) * B * y / n
    equation = sp.Eq(f_Q, Q)
    solutions = sp.nsolve(equation, y, 1)
    return solutions  # water depth 

def estimate_parameters(B, h, Q, s, n, y):
  Area = B * y
  V = Q /Area # velocity 
  wetted_perimeter = B + 2*y   # wetted perimeter
  hydraulic_radius = Area / wetted_perimeter  # R 

  return Area, V,  wetted_perimeter, hydraulic_radius

def check_cross_section(h, y):
  if y<=h:
    return True
  else:
    return False


def plot_rectangle(width, h, thickness, y):
  # Create a new figure
  fig, ax = plt.subplots()

  # Define the rectangle properties
  lower_left_rectangle = (1, 1)  # (x, y) coordinates of the lower-left corner
  color = 'gray'  # Optional color specification
  edgecolor = 'red'  # Optional edge color specification
  linestyle = '--'  # Optional line style for the edge


  # adding the bottom patch
  rectangle = patches.Rectangle(lower_left_rectangle, width, thickness, color=color, edgecolor=edgecolor, linestyle=linestyle)
  ax.add_patch(rectangle)

  # adding left patch
  y_lower_left_corner_left = lower_left_rectangle[1]
  lower_left_corner = (lower_left_rectangle[0]-thickness, y_lower_left_corner_left)
  print(lower_left_corner)
  rectangle = patches.Rectangle(lower_left_corner, thickness, h+thickness, color=color, edgecolor=edgecolor, linestyle=linestyle)
  ax.add_patch(rectangle)

  # adding right patch
  y_lower_right_corner_left = lower_left_rectangle[1] + thickness
  lower_right_corner = (lower_left_rectangle[0]+width, y_lower_left_corner_left)
  print(lower_right_corner)
  rectangle = patches.Rectangle(lower_right_corner, thickness, h+thickness, color=color, edgecolor=edgecolor, linestyle=linestyle)
  ax.add_patch(rectangle)

  # draw water surface
  lower_left_water_rectangle = (lower_left_rectangle[0], lower_left_rectangle[0]+thickness)  # (x, y) coordinates of the lower-left corner
  print(lower_left_water_rectangle)
  water_rectangle = patches.Rectangle(lower_left_water_rectangle, width, y, color='b', edgecolor=edgecolor, linestyle=linestyle)
  ax.add_patch(water_rectangle)

  # Set limits of the plot
  left_limit = lower_left_rectangle[0] - 0.2
  right_limit = lower_left_rectangle[0] +  width + 0.2

  print('before limits')
  plt.xlim(left_limit, right_limit)
  plt.ylim(0, 3)

  # add arrows
  # to be done

  # Add labels and title
  plt.xlabel('X-axis')
  plt.ylabel('Y-axis')
  plt.title('Rectangle Plot')

  # Display the plot
  # plt.grid(True)
  plt.axis('equal')
  plt.xlabel('')
  plt.ylabel('')
  # plt.show()

  plt.savefig('Final_plot.png')

st.set_page_config(layout = "wide")

col2, space2, col3, = st.columns((8,1,10))

# not sure if this is the best application
##if st.session_state["authentication_status"]:

with col2:
    st.write(f" **Rectangular**")
    st.image('final_images/rectangular_plot.png', width=400, caption='Rectangular cross section')
    B = st.text_input(label="width (m)", value="1.50", help='this is the width of the rectangular cross section')
    h = st.text_input(label="height (m)", value="1.00", help='this is the height of the rectangular cross section')
    s = st.text_input(label="slope", value="0.02", help='this is the  is the slope of the channel bed (also known as the energy gradient or hydraulic gradient)')
    Q = st.text_input(label="Discharge (m³/s)",  value="1.00", help="Q is the flow rate")
    n = st.text_input(label="Manning (-)", value="0.012", help='The Manning coefficient, often denoted as "n" is a dimensionless constant used in the Manning\'s \nequation to calculate the flow velocity of water in an open channel. It represents the roughness of the channel bed and banks and influences the resistance to flow.')

    B = float(B)  # Convert input to float
    h = float(h)  # Convert input to float
    s = float(s)  # Convert input to float
    Q = float(Q)  # Convert input to float
    n = float(n)  # Convert input to float

    input_params = {'width (m)': B,
                    'height (h)': h,
                    'slope (-)': s,
                    'discharge (m3/s)': Q,
                    'manning coeffiecient (-)': n
                    }

    with col3:
        st.write(f" **Outputs**")
        print(B)
        y_rect = estimate_rectang_y(B, h, Q, s, n)
        rounded_y_rect = round(y_rect, 3)

        # paramters claculation
        Area, velocity, wetted_perimeter, hydraulic_radius =  estimate_parameters(B, h, Q, s, n, y_rect)
        est_params = Utils.create_dict_est_params(Area, velocity, wetted_perimeter, hydraulic_radius)

        st.write(f" water depth (m) = :blue[**{rounded_y_rect}**]")
        st.write(f" Area (m2)= **{round(Area, 3)}**")
        st.write(f" velocity (m/s)= **{round(velocity, 3)}**")
        st.write(f" wetted_perimeter (m)= **{round(wetted_perimeter, 3)}**")
        st.write(f" hydraulic_radius (m)= **{round(hydraulic_radius, 3)}**")

        if check_cross_section(h, y_rect):
           st.write(f" Is the cross section sufficient? :green[yes]")
        else:
           st.write(f" Is the cross section sufficient? :red[no]")

        # temperature = "-10"
        # st.write(f"temprature: :blue[{temperature}]")

        # add the plot
        thickness = 0.2
        plot_rectangle(B, h, thickness, y_rect)
        st.image('Final_plot.png', width=400, caption='Estimated Rectangular cross section')

        # Report Generation
        now = datetime.now()

        # Format the date and time into one string
        current_datetime = now.strftime("%Y-%m-%d %H:%M")

        # call report - word
        prod_report = Report(type='rectangular', params_input = input_params, params_output = est_params)
        prod_report.add_header('Hydraulic Calculations - '+prod_report.type)
        prod_report.add_footer('Creator: Ilias Machairas', current_datetime)
        text = [
            "The Manning formula is an empirical equation used in fluid mechanics to estimate the flow rate of water in open channels, such as rivers, streams, or canals.",
        ]

        bullet_text = [ "Q is the flow rate (volume of water passing through a cross-section per unit time).",
            "n is the Manning's roughness coefficient (a dimensionless parameter representing the resistance to flow caused by the channel's roughness).",
            "A is the cross-sectional area of flow.",
            "R is the hydraulic radius (the ratio of the cross-sectional area to the wetted perimeter).",
            "S is the slope of the channel bed (also known as the energy gradient or hydraulic gradient)."
        ]

        ## add blanl lines

        # add date-time

        prod_report.add_paragraph(text)
        prod_report.add_bullets(bullet_text)
        prod_report.add_paragraph('')
        prod_report.add_table(2, input_params)
        prod_report.add_paragraph('Below the results are attached')
        prod_report.add_table(2, est_params)
        prod_report.add_paragraph('')

        current_directory = os.getcwd()
        image_path = os.path.join(current_directory, 'Final_plot.png')
        prod_report.add_image(image_path)

        filename = "report_results.docx"
        outpath_report = os.path.join(current_directory, filename)
        prod_report.export_report(outpath_report)

        # export the values to an excel or csv document


        # export to a word document of pdf

        st.markdown(
            '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"/>',
            unsafe_allow_html=True,
        )

        with stylable_container(
                key="container_with_border",
                css_styles=r"""
                button {
                width: 120px; /* Adjust width as needed */
                height: 80px; /* Adjust height as needed */
                height: 80px; /* Adjust height as needed */
                }
                button p:before {
                    font-family: 'Font Awesome 5 Free';
                    content: '\f1c2';
                    display: inline-block;
                    padding-right: 3px;
                    vertical-align: middle;
                    font-weight: 900;
                    font-size: 24px;
                }
                """,
        ):

            # st.download_button("Download")
            with open('report_results.docx', 'rb') as f:
                st.download_button('Download document', f, file_name='report_results.docx',
                                   mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document')