import tkinter
from tkinter import *
import tkintermapview
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import *
import customtkinter
import os
from tkinter.simpledialog import askstring
import sys
import osmnx
import networkx as nx
import numpy as np

customtkinter.set_appearance_mode("dark")

root = customtkinter.CTk()
root.title("Linienverläufe Tool")
root.geometry("1600x900")
root.resizable(True, True)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
root.grid_columnconfigure(5, weight=1)
root.grid_columnconfigure(6, weight=1)
root.grid_columnconfigure(7, weight=1)
root.grid_columnconfigure(8, weight=1)
root.grid_columnconfigure(9, weight=1)
root.grid_columnconfigure(10, weight=1)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_rowconfigure(7, weight=1)
root.grid_rowconfigure(8, weight=1)
root.grid_rowconfigure(9, weight=1)
root.grid_rowconfigure(10, weight=1)
root.grid_rowconfigure(11, weight=1)
root.grid_rowconfigure(12, weight=1)
root.grid_rowconfigure(13, weight=1)
root.grid_rowconfigure(14, weight=1)
root.grid_rowconfigure(15, weight=1)


def on_closing():
    if tkinter.messagebox.askokcancel("Beenden", "Soll das Programm wirklich beendet werden?"):
        root.destroy()
        os.remove("uebergang.xml")
        sys.exit()


def start():
    root.deiconify()
    try:
        start.count = 0
        start.duplicateCount = 0
        start.coordinates = []
        start.deleteCount = 0
        start.deleteArray = []

        Datei = askopenfilename(filetypes=[("xml", "*.xml")], title="Bitte .xml auswählen!")
        Datei2 = open(Datei, 'r')
        Lines = Datei2.readlines()

        for ele in root.winfo_children():
            ele.destroy()

        DateiName = customtkinter.CTkEntry(root, font=("Helvetia", 14), width=200)
        DateiName.grid(column=0, row=0, padx=15, pady=20, sticky="NW")

        DateiNameEnd = os.path.basename(Datei)
        DateiName.insert(END, DateiNameEnd)

        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("Treeview", background="#252525",
                        fieldbackground="#252525", foreground="white")

        columns = ('Nr.', 'Latitude', 'Longitude')
        tree = ttk.Treeview(root, columns=columns, show="headings")
        tree.place(width=200, height=650, relx=1, x=-215, y=20)
        # tree.grid(column=10, row=0, rowspan=12, sticky="E", padx=20, pady=15)

        scroll = customtkinter.CTkScrollbar(root, orientation="vertical", height=653, width=20)
        scroll.configure(command=tree.yview)
        scroll.grid(column=10, row=0, rowspan=12, pady=15, padx=5, sticky="NE")

        tree.configure(yscrollcommand=scroll.set)

        tree.column("Nr.", minwidth=0, width=40, stretch=NO)
        tree.column("Latitude", minwidth=0, width=78, stretch=NO)
        tree.column("Longitude", minwidth=0, width=78, stretch=NO)

        tree.heading('Nr.', text="Nr.")
        tree.heading('Latitude', text="Latitude")
        tree.heading('Longitude', text="Longitude")

        start.duplicateControl = np.array([])

        for index, line in enumerate(Lines):
            mapems = []
            if "<trkseg>" in line:
                start.count += 1
                line = ("".join(Lines[max(0, index + 1):index + 2]))
                positionLine = line.replace("\n", "").replace("</trkpt>", "").replace("<trkpt lat=\"", "").replace(
                    "\" lon=\"", ", ").replace("\">", "").replace("\t", "")
                positionLine = positionLine.split(", ")
                positionLine11 = float(positionLine[0])
                positionLine22 = float(positionLine[1])

                start.coordinates.append((positionLine11, positionLine22))
                mapems.append((start.count, positionLine11, positionLine22))

                for mapems in mapems:
                    tree.insert('', END, values=mapems)

            else:
                if line.__contains__("<trkpt lat=\"5") or line.__contains__("<trkpt lat=\"4"):
                    start.count += 1
                    positionLine = line.replace("\n", "").replace("</trkpt>", "").replace("<trkpt lat=\"", "").replace(
                        "\" lon=\"", ", ").replace("\">", "").replace("\t", "")
                    positionLine = positionLine.split(", ")
                    positionLine1 = float(positionLine[0])
                    positionLine2 = float(positionLine[1])

                    if start.coordinates.__contains__((positionLine1, positionLine2)):
                        start.duplicateCount += 1
                        np.append(start.duplicateControl, start.count)
                        searchVal = start.count - 1
                        ii = np.where(start.duplicateControl == searchVal)[0]

                        if start.coordinates.index((positionLine1, positionLine2)) == start.count - 2:
                            pass
                        if len(ii) < 1:
                            pass

                        else:
                            start.coordinates.append((positionLine1, positionLine2))
                            mapems.append(((start.count - start.duplicateCount), positionLine1, positionLine2))
                            for mapems in mapems:
                                tree.insert('', END, values=mapems)
                    else:

                        start.coordinates.append((positionLine1, positionLine2))
                        mapems.append(((start.count - start.duplicateCount), positionLine1, positionLine2))
                        for mapems in mapems:
                            tree.insert('', END, values=mapems)

        start.n = 0
        start.new_markers = []
        start.xmlAnhang = ""

        def add_marker_event(coords):
            addMarker = []
            start.count += 1
            start.new_markers.append((coords[0], coords[1]))
            start.n = start.n + 1
            addMarker.append((start.count, (coords[0]), (coords[1])))
            start.coordinates.append((coords[0], coords[1]))

            start.xmlAnhang = start.xmlAnhang + "\n<trkpt lat=\"" + str(coords[0]) + "\" lon=\"" + str(
                coords[1]) + "\"></trkpt>"
            start.xmlAnhang = start.xmlAnhang.replace("</gpx>", "")

            path_1.delete()
            map_widget.set_path(start.coordinates)

            for markers in addMarker:
                tree.insert('', END, values=markers)

        def add_marker_event_start(coords):
            addMarkerStart = []
            start.count += 1
            start.new_markers.append((coords[0], coords[1]))
            start.n = start.n + 1
            addMarkerStart.append((1, (coords[0]), (coords[1])))
            start.coordinates.insert(0, (coords[0], coords[1]))

            start.xmlAnhang = start.xmlAnhang + "\n<trkpt lat=\"" + str(coords[0]) + "\" lon=\"" + str(
                coords[1]) + "\"></trkpt>"
            start.xmlAnhang = start.xmlAnhang.replace("</gpx>", "")

            path_1.delete()
            map_widget.set_path(start.coordinates)

            for markersStart in addMarkerStart:
                tree.insert('', 0, values=markersStart)

        def new_marker_behind_current(coords):
            start.count += 1
            curItem = tree.focus()
            nummeraktuell = (tree.item(curItem, 'values')[0])
            start.coordinates.insert(int(nummeraktuell), (coords[0], coords[1]))

            for item in tree.get_children():
                tree.delete(item)

            MarkerBehind = []
            for c in range(0, len(start.coordinates)):
                MarkerBehind.append((c + 1, (start.coordinates[c][0]), (start.coordinates[c][1])))

            for markersBehind in MarkerBehind:
                tree.insert('', END, values=markersBehind)

            path_1.delete()
            map_widget.set_path(start.coordinates)
            id2 = tree.get_children()[int(nummeraktuell)]
            tree.selection_set(id2)
            tree.focus(id2)

        def save_in_datei():
            item = 0

            with open('uebergang.xml', 'w') as f:
                f.write(
                    "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\n<gpx>\n<trk>\n<name>GPX Track fuer Line 1 und Ziel z</name>\n<trkseg>\n")

                for n in range(0, len(start.coordinates)):
                    item += 1
                    f.write(
                        f"<trkpt lat=\"{(start.coordinates[item - 1])[0]}\" lon=\"{(start.coordinates[item - 1])[1]}\"></trkpt>\n")

            open(Datei, 'w').close()

            Datei3 = open('uebergang.xml', 'r')
            Lines2 = Datei3.readlines()

            with open(Datei, 'w') as f:
                for linee in Lines2:
                    f.write(linee)
                else:
                    pass

                f.write("\n</trkseg>\n</trk>\n</gpx>")

            showinfo(title="Gespeichert", message="Die Datei wurde gespeichert!")
            open('uebergang.xml', 'w').close()

        def save_in_neu():
            item = 0
            name = askstring('Neuer Dateiname', 'Wie soll die Datei genannt werden? Leerer Name nicht möglich!')
            if name != "" and name != "None" and name != 0 and name is not None:

                with open(f"{name}.xml", 'w') as f:
                    f.write(
                        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\n<gpx>\n<trk>\n<name>GPX Track fuer Line 1 und Ziel z</name>\n<trkseg>\n")

                    for n in range(0, len(start.coordinates)):
                        item += 1
                        f.write(
                            f"<trkpt lat=\"{(start.coordinates[item - 1])[0]}\" lon=\"{(start.coordinates[item - 1])[1]}\"></trkpt>\n")

                    f.write(start.xmlAnhang + "</trkpt>\n</trkseg>\n</trk>\n</gpx>")
            else:
                pass

        def delete_last():
            if tkinter.messagebox.askokcancel(f"Wirklich löschen",
                                              f"Soll der letzte (unterste) Punkt wirklich gelöscht werden?"):
                del start.coordinates[-1]

        def delete_focused():
            curItem = tree.focus()
            nummerDelete = (tree.item(curItem, 'values')[0])
            latitudeDelete = (tree.item(curItem, 'values')[1])
            longitudeDelete = (tree.item(curItem, 'values')[2])
            if tkinter.messagebox.askokcancel(f"Wirklich löschen",
                                              f"Soll der folgende Punkt wirklich gelöscht werden? \nStelle: {nummerDelete}; lat: {latitudeDelete}, lon: {longitudeDelete}"):
                start.deleteCount += 1
                start.deleteArray.append((tree.item(curItem, 'values')))
                tree.delete(curItem)

                whereToDelete = start.coordinates.index((float(latitudeDelete), float(longitudeDelete)))

                del start.coordinates[whereToDelete]

                path_1.delete()
                map_widget.set_path(start.coordinates)

        def change_marker():
            curItem = tree.focus()
            latitudeChange = (tree.item(curItem, 'values')[1])
            longitudeChange = (tree.item(curItem, 'values')[2])
            dialog = customtkinter.CTkInputDialog(text="Wohin soll der Punkt geändert werden?", title="Punkt ändern", button_fg_color="#404040", button_hover_color="#4d4d4d")
            newName = dialog.get_input()
            if newName != "" or None:
                index2 = start.coordinates.index((float(latitudeChange), float(longitudeChange)))
                newName = newName.split(" ")
                start.coordinates[index2] = (float(newName[0]), float(newName[1]))

            for item in tree.get_children():
                tree.delete(item)

            refreshChange = []
            for x in range(0, len(start.coordinates)):
                refreshChange.append((x + 1, (start.coordinates[x][0]), (start.coordinates[x][1])))

            for changeItemsRefresh in refreshChange:
                tree.insert('', END, values=changeItemsRefresh)

        def zoom_closer(event):
            map_widget.delete_all_marker()
            curItem = tree.focus()
            nummerZoom = (tree.item(curItem, 'values')[0])
            latitudeZoom = (tree.item(curItem, 'values')[1])
            longitudeZoom = (tree.item(curItem, 'values')[2])
            if curItem != "":
                map_widget.set_position(float(latitudeZoom), float(longitudeZoom))
                map_widget.set_zoom(20)
                map_widget.set_marker(float(latitudeZoom), float(longitudeZoom), text=f"{nummerZoom}")

            else:
                pass

        def new_marker_end():
            curItem = tree.focus()
            nummerNew = (tree.item(curItem, 'values')[0])
            coordsNeu = askstring('Welche Koordinaten', 'Koordinaten eingeben (können mit Rechtsclick kopiert werden)!')
            if coordsNeu != "":
                coordsNeu = str(coordsNeu).split(" ")
                start.coordinates.insert((int(nummerNew) + 1), (float(coordsNeu[0]), float(coordsNeu[1])))

                NewMarkerEnd = [((int(nummerNew) + 1), float(coordsNeu[0]), float(coordsNeu[1]))]

                for items in NewMarkerEnd:
                    tree.insert('', start.coordinates.index((float(coordsNeu[0]), float(coordsNeu[1]))) - 1,
                                values=items)

        def show_all_markers():
            if len(start.coordinates) > 200:
                if map_widget.zoom < 13:
                    if tkinter.messagebox.askokcancel(f"Wirklich löschen",
                                                      f"Wirklich alle Marker anzeigen? WARNUNG: Bei vielen Punkten Absturzgefahr!"):
                        map_widget.delete_all_marker()
                        for n in range(0, len(start.coordinates) - 1):
                            map_widget.set_marker(float((start.coordinates[n])[0]), float((start.coordinates[n])[1]),
                                                  text=f"{n + 1}")

                else:
                    map_widget.delete_all_marker()
                    for n in range(0, start.count - 1):
                        map_widget.set_marker(float((start.coordinates[n])[0]), float((start.coordinates[n])[1]),
                                              text=f"{n + 1}")

            else:
                map_widget.delete_all_marker()
                for n in range(0, start.count - 1):
                    map_widget.set_marker(float((start.coordinates[n])[0]), float((start.coordinates[n])[1]),
                                          text=f"{n + 1}")

        def delete_all_markers():
            map_widget.set_zoom(20)
            map_widget.delete_all_marker()
            map_widget.set_zoom(15)

        def delete_all_markers_slow():
            map_widget.delete_all_marker()

        def delete_in_row():
            deleteDialog1 = customtkinter.CTkInputDialog(text="Ab (einschließlich) welcher Nummer soll gelöscht werden?", title="Löschen", button_fg_color="#404040", button_hover_color="#4d4d4d")
            deleteDialog1Answer = deleteDialog1.get_input()

            deleteDialog2 = customtkinter.CTkInputDialog(text="Bis einschließlich welcher Nummer soll gelöscht werden?", title="Löschen", button_fg_color="#404040", button_hover_color="#4d4d4d")
            deleteDialog2Answer = deleteDialog2.get_input()

            if deleteDialog1Answer and deleteDialog2Answer != "" or None:
                for n in range(int(deleteDialog1Answer) - 1, (int(deleteDialog2Answer))):
                    del start.coordinates[int(deleteDialog1Answer) - 1]

            path_1.delete()
            map_widget.set_path(start.coordinates)

            for item in tree.get_children():
                tree.delete(item)

            refreshTree = []
            for c in range(0, len(start.coordinates)):
                refreshTree.append((c + 1, (start.coordinates[c][0]), (start.coordinates[c][1])))

            for treeItemsRefresh in refreshTree:
                tree.insert('', END, values=treeItemsRefresh)


        def auto_complete_line():

            answer = askyesno(title='Wirklich vervollständigen?',
                              message='Wirklich vervollständigen?\n\nDauer je nach Größe und Cache 1-5 Minuten\n\n!System may be unresponsive!')
            if answer:

                print(start.coordinates)

                point = []

                place = 'Kassel, Hesse, Germany'
                mode = 'drive'
                optimizer = 'length'

                osmnx.settings.log_console = True
                osmnx.settings.use_cache = True

                graph = osmnx.graph_from_place(place, network_type=mode, simplify=True, retain_all=True,
                                               buffer_dist=30000)

                Gs = osmnx.utils_graph.get_largest_component(graph, strongly=True)

                for n in range(0, len(start.coordinates)):
                    osmnxInsert = osmnx.nearest_nodes(Gs, start.coordinates[n][1], start.coordinates[n][0])
                    if osmnxInsert != 0:
                        point.append(osmnxInsert)
                    else:
                        pass

                point = list(dict.fromkeys(point))

                name = Datei.replace(".xml", "")
                f = open(f"{name}-generated.xml", "a")
                f.write("""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<gpx>
<trk>
<name>GPX Track fuer Line 1 und Ziel z</name>
<trkseg>
<trkpt lat=\"""")

                try:
                    for n in range(0, len(point)):
                        print(point[n], point[n + 1])
                        shortest_route = nx.shortest_path(graph, point[n], point[n + 1], weight=optimizer)
                        route_map = osmnx.plot_route_folium(graph, shortest_route)
                        route_map.save(f'{name}-{n}-generatedThrowaway.xml')

                        dateiRead = open(f'{name}-{n}-generatedThrowaway.xml', 'r')
                        linesRead = dateiRead.readlines()

                        for lines in linesRead:
                            if "51." in lines and "9." in lines and "center" not in lines:
                                if len(lines) < 88:
                                    pass
                                else:
                                    lines = lines.replace("], ", "\"></trkpt>\n<trkpt lat=\"").replace("[", "").replace(
                                        "                ", "").replace("]],", "\"></trkpt>\n<trkpt lat=\"").replace(
                                        ", ", "\" lon=\"").replace("\n", "")
                                    lines = lines.replace("<trkpt", "\n<trkpt")
                                    f.write(lines)
                            else:
                                pass

                except (ValueError, NameError, IndexError):
                    pass

                f.write("""\n</trkseg>
</trk>
</gpx>""")
                f.close()

                try:
                    for n in range(0, 500):
                        dateiRead = open(f'{name}-{n}-generatedThrowaway.xml', 'r')
                        dateiRead.close()
                        os.remove(f'{name}-{n}-generatedThrowaway.xml')
                except (ValueError, NameError, IndexError):
                    pass

            else:
                pass

        m = Menu(root, tearoff=0)
        m.add_command(label="ausgewählten Punkt löschen", command=lambda: delete_focused())
        m.add_command(label="neuer Punkt hinter Auswahl", command=lambda: new_marker_end())
        m.add_separator()
        m.add_command(label="Ändern", command=lambda: change_marker())

        def show_options(event):
            try:
                m.tk_popup(event.x_root, event.y_root)
            finally:
                m.grab_release()

        my_label = LabelFrame(root, height=850, width=1100)
        my_label.grid(column=1, row=0, columnspan=9, rowspan=15)

        map_widget = tkintermapview.TkinterMapView(my_label, width=1100, height=850, corner_radius=0)
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                        max_zoom=22)  # google satellite
        map_widget.grid(column=1, row=0, columnspan=9, rowspan=15, sticky="NS")
        map_widget.set_position(positionLine11, positionLine22)
        map_widget.set_zoom(12)

        path_1 = map_widget.set_path(start.coordinates)

        map_widget.add_right_click_menu_command(label="Punkt am Ende hinzufügen",
                                                command=add_marker_event,
                                                pass_coords=True)

        map_widget.add_right_click_menu_command(label="Punkt am Anfang hinzufügen",
                                                command=add_marker_event_start,
                                                pass_coords=True)

        map_widget.add_right_click_menu_command(label="Punkt hinter aktueller Auswahl",
                                                command=new_marker_behind_current,
                                                pass_coords=True)

        button = customtkinter.CTkButton(root, text="Neue .xml auswählen", command=lambda: start(), width=200, fg_color="#404040", hover_color="#4d4d4d")
        button.grid(column=0, row=1, padx=15, pady=5, sticky="NW")

        buttonclose = customtkinter.CTkButton(root, text="Beenden", command=lambda: on_closing(), width=200, fg_color="#404040", hover_color="#4d4d4d")
        buttonclose.grid(column=0, row=1, padx=15, pady=5, sticky="SW")

        button = customtkinter.CTkButton(root, text="Punkte markieren", command=lambda: show_all_markers(), width=200, fg_color="#404040", hover_color="#4d4d4d")
        button.grid(column=0, row=3, padx=15, pady=5, sticky="NW")

        button = customtkinter.CTkButton(root, text="Marker entfernen\n(schnell)", command=lambda: delete_all_markers(), width=200, height=40, fg_color="#404040", hover_color="#4d4d4d")
        button.grid(column=0, row=4, padx=15, pady=5, sticky="NW")

        button = customtkinter.CTkButton(root, text="Marker entfernen\n(langsam)", command=lambda: delete_all_markers_slow(), width=200, height=40, fg_color="#404040", hover_color="#4d4d4d")
        button.grid(column=0, row=5, padx=15, pady=5, sticky="NW")

        button = customtkinter.CTkButton(root, text="Automatisch vervollständigen", command=lambda: auto_complete_line(), width=200, fg_color="#404040", hover_color="#4d4d4d")
        button.grid(column=0, row=6, padx=15, pady=5, sticky="NW")

        button = customtkinter.CTkButton(root, text="Speichern", command=lambda: save_in_datei(), width=200, fg_color="#404040", hover_color="#4d4d4d")
        button.grid(column=0, row=7, padx=15, pady=5, sticky="NW")

        button = customtkinter.CTkButton(root, text="Speichern in Neu", command=lambda: save_in_neu(), width=200, fg_color="#404040", hover_color="#4d4d4d")
        button.grid(column=0, row=7, padx=15, pady=5, sticky="SW")

        button = customtkinter.CTkButton(root, text="Auswahl löschen", command=lambda: delete_focused(), width=200, fg_color="#404040", hover_color="#4d4d4d")
        button.grid(column=10, row=10, padx=15, pady=5, sticky="S")

        button = customtkinter.CTkButton(root, text="Letzte löschen", command=lambda: delete_last(), width=200, fg_color="#404040", hover_color="#4d4d4d")
        button.grid(column=10, row=11, padx=15, pady=5, sticky="N")

        button = customtkinter.CTkButton(root, text="Punkte fortlaufend löschen", command=lambda: delete_in_row(), width=200, fg_color="#404040", hover_color="#4d4d4d")
        button.grid(column=10, row=11, padx=15, pady=15, sticky="S")

        img = PhotoImage(file="C://Users//Friedrich//Desktop/sad_Logo_CMYK_helle_Schrift_ipk_trans.png")
        Test = Label(master=root, image=img, bg="#242424", width=200, height=250)
        Test.grid(column=0, row=9, padx=15, pady=5, rowspan=5, columnspan=1, sticky="NW")

        tree.bind('<Double-Button-1>', zoom_closer)
        tree.bind('<Button-3>', show_options)

        root.protocol("WM_DELETE_WINDOW", lambda: on_closing())

        root.mainloop()

    except(RuntimeError, TypeError, NameError):
        root.withdraw()
        tkinter.messagebox.showerror(title="Error", message="Es gibt einen Fehler mit der Datei, bitte neu auswählen")
        start()


start()

