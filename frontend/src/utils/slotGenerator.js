/**
 * Převede souvislé intervaly na pole 60minutových slotů
 */
export function generateHourlySlots(availabilityList) {
  const hourlySlots = [];

  availabilityList.forEach((item) => {
    let currentStart = new Date(item.start);
    const itemEnd = new Date(item.end);

    while (currentStart < itemEnd) {
      const nextHour = new Date(currentStart.getTime() + 60 * 60 * 1000);

      if (nextHour <= itemEnd) {
        // Získáme YYYY-MM-DD přímo z textu nebo z lokálního času
        const year = currentStart.getFullYear();
        const month = String(currentStart.getMonth() + 1).padStart(2, '0');
        const day = String(currentStart.getDate()).padStart(2, '0');
        const dateKey = `${year}-${month}-${day}`;

        const startHour = String(currentStart.getHours()).padStart(2, '0');
        const endHour = String(nextHour.getHours()).padStart(2, '0');

        hourlySlots.push({
          slot_id: `${item.slot_id}_${currentStart.getTime()}`,
          original_slot_id: item.slot_id,
          person_id: item.person_id,
          start: new Date(currentStart),
          end: new Date(nextHour),
          dateKey: dateKey,
          timeKey: `${startHour}:00`,
          label: `${startHour}:00 - ${endHour}:00`,
        });
      }

      currentStart = nextHour;
    }
  });

  return hourlySlots;
}