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
import math
from datetime import datetime

def estimate_circular_theta(r, Q, s, n, initial_sol):
    theta = sp.symbols('theta')
    D = 2 * r
    A = D**2 /8 * (theta - sp.sin(theta))
    P = D * theta /2
    R = A /P
    # equation
    f_Q = (1/n) * (A) * R**(2/3) * s**0.5
    equation = sp.Eq(f_Q, Q)
    solutions = sp.nsolve(equation, theta, initial_sol)

    return solutions


def estimate_circular_y_n(r, theta):
    D = 2 * r
    y_n = D / 2 * (1 - sp.cos(theta / 2))
    return y_n


def estimate_parameters(r, Q, s, n, theta):
    D = 2 * r
    Area = D**2 /8 * (theta - sp.sin(theta))
    wetted_perimeter = D * theta /2
    hydraulic_radius = Area / wetted_perimeter
    V = Q / Area  # velocity

    return Area, V,  wetted_perimeter, hydraulic_radius


def check_cross_section(r, y):
    D = 2* r
    if y<=D:
        return True
    else:
        return False

def degree2rad(degrees):
    return degrees*np.pi/180

def estimate_circular_pipe(x0, y0, r, theta):
  circle1 = plt.Circle((x0, y0), r, fill=None, edgecolor='gray',)
  circle2 = plt.Circle((x0, y0), r+0.02, fill=None, edgecolor='gray', linewidth=20)

   # note we must use plt.subplots, not plt.subplot
  # (or if you have an existing figure)
  # fig = plt.gcf()
  # ax = fig.gca()

  print(math.degrees(theta))
  if math.degrees(theta) >= 180:
    print('condition 1')
    residual_deg = math.degrees(theta) - 180
    theta1 = np.linspace(0, residual_deg/2, 100)
    x = x0+r*np.cos(degree2rad(theta1))
    y = y0+r*np.sin(degree2rad(theta1))

    theta2 = np.linspace(180-residual_deg/2, 360, 100)
    x2 = x0+ r*np.cos(degree2rad(theta2))
    y2 = y0+ r*np.sin(degree2rad(theta2))

    pairs = np.column_stack((x, y))
    pairs_2 = np.column_stack((x2, y2))
    comb_pairs = np.concatenate((pairs, pairs_2))
  else:
    residual_deg = 180  - math.degrees(theta)
    theta3 = np.linspace(180+residual_deg/2, 360 - residual_deg/2, 100)
    print(180+residual_deg/2, 360 - residual_deg/2)
    x3 = x0+r*np.cos(degree2rad(theta3))
    y3 = y0+r*np.sin(degree2rad(theta3))
    comb_pairs = np.column_stack((x3, y3))

  p = Polygon(comb_pairs, facecolor = 'blue')
  return circle1, circle2, p

def plot_circular_pipe(x0, y0, r, theta, y):
  fig, ax = plt.subplots()
  c1, c2, p = estimate_circular_pipe(x0, y0, r, theta)
  ax.add_patch(p)
  ax.add_patch(c1)
  ax.add_patch(c2)
  plt.axis('equal')
  # plt.axis('off')

  plt.savefig('Final_plot.png')


def plot_twin_circular_pipe(x0, y0, r, theta, y):
  fig, ax = plt.subplots()
  c1, c2, p1 = estimate_circular_pipe(x0, y0, r, theta)
  # estimate
  x1 = x0 + 2*r + 2*0.02 + 0.5
  y1 = y0
  c3, c4, p2 = estimate_circular_pipe(x1, y1, r, theta)
  ax.add_patch(p1)
  ax.add_patch(c1)
  ax.add_patch(c2)

  ax.add_patch(p2)
  ax.add_patch(c3)
  ax.add_patch(c4)
  plt.axis('equal')
  #plt.show()
  #plt.axis('off')
  plt.savefig('Final_plot.png')

# def plot_circular_pipe(x0, y0, r, theta):
#   circle1 = plt.Circle((x0, y0), r, fill=None, edgecolor='gray',)
#   circle2 = plt.Circle((x0, y0), r+0.02, fill=None, edgecolor='gray', linewidth=20)
#
#   fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
#   # (or if you have an existing figure)
#   # fig = plt.gcf()
#   # ax = fig.gca()
#
#   print(math.degrees(theta))
#   if math.degrees(theta) >= 180:
#     print('condition 1')
#     residual_deg = math.degrees(theta) - 180
#     theta1 = np.linspace(0, residual_deg/2, 100)
#     x = x0+r*np.cos(degree2rad(theta1))
#     y = y0+r*np.sin(degree2rad(theta1))
#
#     theta2 = np.linspace(180-residual_deg/2, 360, 100)
#     x2 = x0+ r*np.cos(degree2rad(theta2))
#     y2 = y0+ r*np.sin(degree2rad(theta2))
#
#     pairs = np.column_stack((x, y))
#     pairs_2 = np.column_stack((x2, y2))
#     comb_pairs = np.concatenate((pairs, pairs_2))
#   else:
#     residual_deg = 180  - math.degrees(theta)
#     theta3 = np.linspace(180+residual_deg/2, 360 - residual_deg/2, 100)
#     print(180+residual_deg/2, 360 - residual_deg/2)
#     x3 = x0+r*np.cos(degree2rad(theta3))
#     y3 = y0+r*np.sin(degree2rad(theta3))
#     comb_pairs = np.column_stack((x3, y3))
#
#   p = Polygon(comb_pairs, facecolor = 'b')
#   ax.add_patch(p)
#
#   ax.add_patch(circle1)
#   ax.add_patch(circle2)
#   plt.axis('equal')
#
#   plt.savefig('Final_plot.png')

st.set_page_config(layout = "wide")

tab1, tab2,  = st.tabs(["Circular ", "Twin Circular"])
with tab1:
    col2, space2, col3, = st.columns((8,1,10))

    with col2:
        st.write(f" **Circular**")
        st.image('final_images/circular_plot.png', width=400, caption='Circular cross section')
        D = st.text_input(label="Diameter (m)", value="1.00", help='this is circular pipe\'s diameter', key='D_pipe_1')
        s = st.text_input(label="slope", value="0.02", key='s_pipe_1', help='this is the  is the slope of the channel bed (also known as the energy gradient or hydraulic gradient)')
        Q = st.text_input(label="Discharge (m³/s)",  value="1.00", key='Q_pipe_1',  help="Q is the flow rate")
        n = st.text_input(label="Manning (-)", value="0.012", key='n_pipe_1', help='The Manning coefficient, often denoted as "n" is a dimensionless constant used in the Manning\'s \nequation to calculate the flow velocity of water in an open channel. It represents the roughness of the channel bed and banks and influences the resistance to flow.')

        D = float(D)  # Convert input to float
        r = D/2
        s = float(s)  # Convert input to float
        Q = float(Q)  # Convert input to float
        n = float(n)  # Convert input to float

        input_params = {'Diameter (m)': D,
                        'slope (-)': s,
                        'discharge (m3/s)': Q,
                        'manning coeffiecient (-)': n
                        }

        with col3:
            st.write(f" **Outputs**")
            ## there is a gap pregarding circular  pipe - estimating theta - initial value
            try:
                est_theta = estimate_circular_theta(r, Q, s, n, initial_sol=3)
            except Exception as e:
                print(e)
                est_theta = estimate_circular_theta(r, Q, s, n, initial_sol=4)
            y_circ = estimate_circular_y_n(r, est_theta)
            rounded_y_circ = round(y_circ, 3)

            # paramters claculation
            Area, velocity, wetted_perimeter, hydraulic_radius =  estimate_parameters(r, Q, s, n, est_theta)
            est_params = Utils.create_dict_est_params(Area, velocity, wetted_perimeter, hydraulic_radius)

            st.write(f" water depth (m) = :blue[**{rounded_y_circ}**]")
            st.write(f" Area (m2)= **{round(Area, 3)}**")
            st.write(f" velocity (m/s)= **{round(velocity, 3)}**")
            st.write(f" wetted_perimeter (m)= **{round(wetted_perimeter, 3)}**")
            st.write(f" hydraulic_radius (m)= **{round(hydraulic_radius, 3)}**")

            if check_cross_section(r, y_circ):
               st.write(f" Is the cross section sufficient? :green[yes]")
            else:
               st.write(f" Is the cross section sufficient? :red[no]")



            # add the plot
            thickness = 0.2
            plot_circular_pipe(1, 1, r, est_theta, y_circ)
            st.image('Final_plot.png', width=400, caption='Estimated Rectangular cross section')

            now = datetime.now()

            # Format the date and time into one string
            current_datetime = now.strftime("%Y-%m-%d %H:%M")

            # call report - word
            prod_report = Report(type='rectangular', params_input=input_params, params_output=est_params)
            prod_report.add_header('Hydraulic Calculations - ' + prod_report.type)
            prod_report.add_footer('Creator: Ilias Machairas', current_datetime)
            text = [
                "The Manning formula is an empirical equation used in fluid mechanics to estimate the flow rate of water in open channels, such as rivers, streams, or canals.",
            ]

            bullet_text = ["Q is the flow rate (volume of water passing through a cross-section per unit time).",
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
                    st.download_button('Download document', f, file_name='report_results.docx', key='download_1',
                                       mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

with tab2:
    col2, space2, col3, = st.columns((8, 1, 10))

    with col2:
        st.write(f" **Twin Circular**")
        st.image('final_images/circular_plot_twin.png', width=400, caption='Circular cross section')
        D = st.text_input(label="Diameter (m)", value="1.00", help='this is circular pipe\'s diameter', key='D_pipe_2')
        s = st.text_input(label="slope", value="0.02", key='s_pipe_2', help='this is the  is the slope of the channel bed (also known as the energy gradient or hydraulic gradient)')
        Q = st.text_input(label="Discharge (m³/s)", value="1.00", key='Q_pipe_2', help="Q is the flow rate")
        n = st.text_input(label="Manning (-)", value="0.012", key='n_pipe_2',
                          help='The Manning coefficient, often denoted as "n" is a dimensionless constant used in the Manning\'s \nequation to calculate the flow velocity of water in an open channel. It represents the roughness of the channel bed and banks and influences the resistance to flow.')

        D = float(D)  # Convert input to float
        r = D / 2
        s = float(s)  # Convert input to float
        Q = float(Q)  # Convert input to float
        n = float(n)  # Convert input to float

        input_params = {'Diameter (m)': D,
                        'slope (-)': s,
                        'discharge (m3/s)': Q,
                        'manning coeffiecient (-)': n
                        }

        with col3:
            st.write(f" **Outputs**")
            ### Attention: I used Q/2 instead of Q
            ## there is a gap pregarding circular  pipe - estimating theta - initial value
            try:
                est_theta = estimate_circular_theta(r, Q/2, s, n, initial_sol=3)
            except Exception as e:
                print(e)
                est_theta = estimate_circular_theta(r, Q/2, s, n, initial_sol=4)
            y_circ = estimate_circular_y_n(r, est_theta)
            rounded_y_circ = round(y_circ, 3)

            # paramters claculation
            Area, velocity, wetted_perimeter, hydraulic_radius = estimate_parameters(r, Q/2, s, n, est_theta)
            est_params = Utils.create_dict_est_params(Area, velocity, wetted_perimeter, hydraulic_radius)

            st.write(f" water depth (m) = :blue[**{rounded_y_circ}**]")
            st.write(f" Area (m2)= **{round(Area, 3)}**")
            st.write(f" velocity (m/s)= **{round(velocity, 3)}**")
            st.write(f" wetted_perimeter (m)= **{round(wetted_perimeter, 3)}**")
            st.write(f" hydraulic_radius (m)= **{round(hydraulic_radius, 3)}**")

            if check_cross_section(r, y_circ):
                st.write(f" Is the cross section sufficient? :green[yes]")
            else:
                st.write(f" Is the cross section sufficient? :red[no]")

            # add the plot
            thickness = 0.2
            plot_twin_circular_pipe(1, 1, r, est_theta, y_circ)
            st.image('Final_plot.png', width=400, caption='Estimated Rectangular cross section')

            now = datetime.now()

            # Format the date and time into one string
            current_datetime = now.strftime("%Y-%m-%d %H:%M")

            # call report - word
            prod_report = Report(type='rectangular', params_input=input_params, params_output=est_params)
            prod_report.add_header('Hydraulic Calculations - ' + prod_report.type)
            prod_report.add_footer('Creator: Ilias Machairas', current_datetime)
            text = [
                "The Manning formula is an empirical equation used in fluid mechanics to estimate the flow rate of water in open channels, such as rivers, streams, or canals.",
            ]

            bullet_text = ["Q is the flow rate (volume of water passing through a cross-section per unit time).",
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
                    st.download_button('Download document', f, file_name='report_results.docx', key='download_2',
                                       mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document')