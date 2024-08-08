import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from streamlit_extras.stylable_container import stylable_container
from Report.report import Report
from Report.Utils import Utils
import os
from datetime import datetime

def estimate_trapezoid_y(B, Q, s, m, n):
  y = sp.symbols('y')
  R_nom = (B + m *y)*y
  R_denom = B + 2*y*np.sqrt(1+m**2)
  R = R_nom / R_denom
  f_Q = R**(2/3) * (s**0.5) / n * (B + m *y)*y
  equation = sp.Eq(f_Q, Q)
  solutions = sp.nsolve(equation, y, 1)
  return solutions


def estimate_parameters(B, Q, s, m, n, y):
  Area = (B + m * y)*y
  V = Q /Area # velocity
  wetted_perimeter =  B + 2*y*np.sqrt(1+m**2)   # wetted perimeter
  hydraulic_radius = Area / wetted_perimeter  # R

  return Area, V,  wetted_perimeter, hydraulic_radius


def check_cross_section(h, y):
    if y <= h:
        return 'yes'
    else:
        return 'no'

def plot_trapezoidal(m, width, B, h, y):
  # find low angle
  theta_low = np.arctan(1/m)
  suppl_theta_low = np.pi/2 - theta_low
  hypotenus_low =  width / np.sin(suppl_theta_low)

  # find upper angle
  hypotenus_high =  width / np.sin(theta_low)

  # right parth
  point_1 = [B/2,0]
  point_2 = [point_1[0]+ h*m, point_1[1]+h]
  point_3 = [point_2[0]+ hypotenus_high, point_1[1]+h]
  point_4 = [point_1[0], point_1[1] - hypotenus_low]
  points_all_right = [point_1, point_2, point_3, point_4, point_1]

  # left part
  point_l1 = [-B/2,0]
  point_l2 = [point_l1[0]- h*m, point_l1[1]+h]
  point_l3 = [point_l2[0] - hypotenus_high, point_l1[1]+h]
  point_l4 = [point_l1[0], point_l1[1] - hypotenus_low]
  points_all_left = [point_l1, point_l2, point_l3, point_l4, point_l1]

  # polygon_part
  point_pol_1 = [-B/2,0]
  point_pol_2 = [B/2,0]
  point_pol_3 = [B/2, -hypotenus_low]
  point_pol_4 = [-B/2, -hypotenus_low]
  points_all_rectangle = [point_pol_1, point_pol_2, point_pol_3, point_pol_4, point_pol_1]

  points_all = [point_l3,  point_l2, point_l1 , point_1, point_2, point_3, point_4, point_l4, point_l3]

  # plot water body
  wb_1 = [- y*np.tan(suppl_theta_low) -B/2, y]
  wb_2 = [y*np.tan(suppl_theta_low)+B/2, y]
  wb_3 = [B/2, 0]
  wb_4 = [- B/2, 0]
  points_water_body = [wb_1, wb_2, wb_3, wb_4, wb_1]

  # p_right = Polygon(points_all_right, facecolor = 'k')
  # p_left =  Polygon(points_all_left, facecolor = 'k')
  # p_rectangle =  Polygon(points_all_rectangle, facecolor = 'k')
  p_all =  Polygon(points_all, facecolor = 'gray')
  p_water_body = Polygon(points_water_body, facecolor = 'b')

  fig, ax = plt.subplots()
  # ax.add_patch(p_right)
  # ax.add_patch(p_left)
  # ax.add_patch(p_rectangle)
  ax.add_patch(p_all)
  ax.add_patch(p_water_body)
  plt.axis('equal')

  # plt.axis('off')
  plt.savefig('Final_plot.png')

st.set_page_config(layout = "wide")

col2, space2, col3, = st.columns((8,1,10))

with col2:
    st.write(f" **Trapezoidal**")
    st.image('final_images/trapezoidal-cross-section.png', width=400, caption='Traqpezoid cross section')
    B = st.text_input(label="width (m)", value="1.0", help='this is the width of the trapezoidal cross section')
    h = st.text_input(label="height (m)", value="0.5", help='this is the height of the rectangular cross section')
    s = st.text_input(label="slope", value="0.02", help='this is the  is the slope of the channel bed (also known as the energy gradient or hydraulic gradient)')
    Q = st.text_input(label="Discharge (m³/s)",  value="1.00", help="Q is the flow rate")
    m = st.text_input(label="m (-)", value="1", help='m is the slope of the line (change in y:1/change in x)')
    n = st.text_input(label="Manning (-)", value="0.012", help='The Manning coefficient, often denoted as "n" is a dimensionless constant used in the Manning\'s \nequation to calculate the flow velocity of water in an open channel. It represents the roughness of the channel bed and banks and influences the resistance to flow.')


    B = float(B)  # Convert input to float
    h = float(h)  # Convert input to float
    s = float(s)  # Convert input to float
    Q = float(Q)  # Convert input to float
    m = float(m)  # Convert input to float
    n = float(n)  # Convert input to float

    input_params = {'width (m)': B,
                    'height (h)': h,
                    'slope (-)': s,
                    'discharge (m3/s)': Q,
                    'm (-)': m,
                    'manning coeffiecoent (-)': n
                    }

    with col3:
        st.write(f" **Outputs**")
        print(B)
        y_rect = estimate_trapezoid_y(B, Q, s, m, n)
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


        thickness = 0.2
        plot_trapezoidal(m, thickness, B, h, y_rect)
        st.image('Final_plot.png', width=400, caption='Estimated trapezoidal cross section')


        now = datetime.now()

        # Format the date and time into one string
        current_datetime = now.strftime("%Y-%m-%d %H:%M")

        # call report - word
        prod_report = Report(type='trapezoidal', params_input = input_params, params_output = est_params)
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